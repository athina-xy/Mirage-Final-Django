from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserProfileForm
from core.models import WishlistItem, Item, Order, OrderItem
from core.views import _get_cart


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You are now logged in.")
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def dashboard_view(request):
    wishlist_items = (
        WishlistItem.objects.filter(user=request.user)
        .select_related("item")
        .order_by("-created_at")
    )

    cart = _get_cart(request.session)
    item_ids = [int(k) for k in cart.keys()]
    items = Item.objects.filter(id__in=item_ids)

    cart_items = []
    cart_total = 0
    for item in items:
        qty = cart.get(str(item.id), 0)
        if qty <= 0:
            continue
        line_total = item.price * qty
        cart_total += line_total
        cart_items.append(
            {
                "item": item,
                "quantity": qty,
                "line_total": line_total,
            }
        )

    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-created_at")[:5]
    )

    context = {
        "wishlist_items": wishlist_items,
        "cart_items": cart_items,
        "cart_total": cart_total,
        "orders": orders,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order).select_related("item")

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, "accounts/order_detail.html", context)
