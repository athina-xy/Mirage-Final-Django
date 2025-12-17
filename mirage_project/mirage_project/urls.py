from django.contrib import admin
from django.urls import path, include

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts app
    path("accounts/", include("accounts.urls")),
    path("", include("core.urls")),

    # Wishlist toggle
    path("wishlist/toggle/<int:item_id>/", core_views.toggle_wishlist, name="toggle_wishlist"),

    # Cart routes
    path("cart/", core_views.view_cart, name="view_cart"),
    path("cart/add/<int:item_id>/", core_views.add_to_cart, name="add_to_cart"),
    path("cart/decrement/<int:item_id>/", core_views.decrement_cart_item, name="decrement_cart_item"),
    path("cart/remove/<int:item_id>/", core_views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", core_views.clear_cart, name="clear_cart"),
    path("cart/checkout/", core_views.checkout, name="checkout"),

    # Pages
    path("catalogue/", core_views.catalogue, name="catalogue"),
    path("", core_views.home, name="home"),
]
