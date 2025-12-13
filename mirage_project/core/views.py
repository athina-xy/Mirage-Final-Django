from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, SubCategory, Item, WishlistItem, Order, OrderItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

# Create your views here.
def home(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    subcategory_slug = request.GET.get('subcategory', '').strip()
    rarity = request.GET.get('rarity', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    items = Item.objects.all().order_by('-created_at')

    # Search
    if query:
        items = items.filter(
            Q(label__icontains=query) |
            Q(description__icontains=query) |
            Q(element__icontains=query) |
            Q(reality_fragment__icontains=query)
        )

    # Category filter
    if category_slug:
        items = items.filter(category__url_name=category_slug)

    # Subcategory filter
    if subcategory_slug:
        items = items.filter(subcategory__url_name=subcategory_slug)

    # Rarity filter
    if rarity:
        items = items.filter(rarity=rarity)

    # Price range
    if min_price:
        # ignore long input
        if len(min_price) <= 6:
            try:
                items = items.filter(price__gte=float(min_price))
            except ValueError:
                pass
    if max_price:
        if len(max_price) <= 6:
            try:
                items = items.filter(price__lte=float(max_price))
            except ValueError:
                pass

    categories = Category.objects.all().order_by('label')
    subcategories = SubCategory.objects.all().order_by('label')

    # which items this user has wishlisted
    wishlist_ids = set()
    if request.user.is_authenticated:
        wishlist_ids = set(
            WishlistItem.objects.filter(user=request.user)
            .values_list("item_id", flat=True)
        )

    # 🔹 NEW: cart count for floating button / header
    cart = _get_cart(request.session)
    cart_count = 0
    for qty in cart.values():
        try:
            cart_count += int(qty)
        except (TypeError, ValueError):
            continue

    context = {
        'items': items,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': category_slug,
        'selected_subcategory': subcategory_slug,
        'selected_rarity': rarity,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'wishlist_ids': wishlist_ids,
        'cart_count': cart_count,   # 🔹 NEW
    }
    return render(request, 'core/home.html', context)


@login_required
def toggle_wishlist(request, item_id):
    """Add or remove an item from the logged-in user's wishlist."""
    item = get_object_or_404(Item, pk=item_id)
    existing = WishlistItem.objects.filter(user=request.user, item=item)

    if existing.exists():
        existing.delete()
        messages.info(request, f"{item.label} removed from your wishlist.")
    else:
        WishlistItem.objects.create(user=request.user, item=item)
        messages.success(request, f"{item.label} added to your wishlist.")

    return redirect('home')


def _get_cart(session):
    """
    Return cart dict from session.
    Structure: {"item_id": quantity, ...}
    """
    return session.get("cart", {})


def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True


def add_to_cart(request, item_id):
    """
    Add one unit of the given item to the cart.
    """
    if request.method != "POST":
        return redirect('home')

    # item validation
    item = get_object_or_404(Item, pk=item_id)

    cart = _get_cart(request.session)
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
    _save_cart(request.session, cart)

    # Optionally show a small message
    messages.success(request, f"{item.label} was added to your cart.")

    # Go back to where the user was
    return redirect(request.META.get("HTTP_REFERER", 'home'))


def view_cart(request):
    """
    Show current cart contents.
    """
    cart = _get_cart(request.session)

    if not cart:
        context = {
            "cart_items": [],
            "cart_total": Decimal("0.00"),
            "cart_count": 0,  # 🔹 NEW
        }
        return render(request, "core/cart.html", context)

    item_ids = [int(k) for k in cart.keys()]
    items = Item.objects.filter(id__in=item_ids)

    cart_items = []
    total = Decimal("0.00")
    cart_count = 0  # 🔹 NEW

    for item in items:
        quantity = cart.get(str(item.id), 0)
        if quantity <= 0:
            continue
        line_total = item.price * quantity
        total += line_total
        cart_count += int(quantity)  # 🔹 NEW

        cart_items.append(
            {
                "item": item,
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    context = {
        "cart_items": cart_items,
        "cart_total": total,
        "cart_count": cart_count,  # 🔹 NEW
    }
    return render(request, "core/cart.html", context)


def remove_from_cart(request, item_id):
    """
    Remove an item entirely from the cart.
    """
    if request.method != "POST":
        return redirect('view_cart')

    cart = _get_cart(request.session)
    cart.pop(str(item_id), None)
    _save_cart(request.session, cart)
    return redirect('view_cart')


def clear_cart(request):
    """
    Empty the cart.
    """
    if request.method != "POST":
        return redirect('view_cart')

    _save_cart(request.session, {})
    return redirect('view_cart')


@login_required
def checkout(request):
    """
    Convert the current cart into an Order + OrderItems.
    """
    cart = _get_cart(request.session)
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method != "POST":
        # Only allow POST to actually create orders
        return redirect('view_cart')

    item_ids = [int(k) for k in cart.keys()]
    items = Item.objects.filter(id__in=item_ids)

    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect('view_cart')

    total = Decimal("0.00")
    order = Order.objects.create(
        user=request.user,
        status="completed",
        total_price=Decimal("0.00"),
    )

    for item in items:
        quantity = cart.get(str(item.id), 0)
        if quantity <= 0:
            continue

        line_total = item.price * quantity
        total += line_total

        OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity,
            price_at_purchase=item.price,
        )

    order.total_price = total
    order.save()

    # Clear cart after successful checkout
    _save_cart(request.session, {})

    return render(request, "core/checkout_success.html", {"order": order})
