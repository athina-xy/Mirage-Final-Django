from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, SubCategory, Item, WishlistItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
