from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserProfileForm
from core.models import WishlistItem, Item


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You are now logged in.")
            return redirect("dashboard")
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
            return redirect("dashboard")
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
    # Wishlist items
    wishlist_items = (
        WishlistItem.objects.filter(user=request.user)
        .select_related("item")
        .order_by("-created_at")
    )

    # Cart from session
    cart_session = request.session.get("cart", {})
    cart_items = []
    cart_total = Decimal("0.00")
    cart_count = 0

    if isinstance(cart_session, dict) and cart_session:
        item_ids = [int(pk) for pk in cart_session.keys()]
        items = Item.objects.filter(id__in=item_ids)

        for item in items:
            quantity = cart_session.get(str(item.id), 0)
            if quantity <= 0:
                continue
            line_total = item.price * quantity
            cart_total += line_total
            cart_count += quantity
            cart_items.append(
                {
                    "item": item,
                    "quantity": quantity,
                    "line_total": line_total,
                }
            )

    context = {
        "wishlist_items": wishlist_items,
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_count": cart_count,   # also used by floating button
    }
    return render(request, "accounts/dashboard.html", context)
