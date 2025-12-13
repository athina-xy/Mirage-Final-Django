from django.contrib import admin
from .models import Category, SubCategory, Item, WishlistItem, Order, OrderItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "url_name")
    prepopulated_fields = {"url_name": ("label",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "category", "url_name")
    list_filter = ("category",)
    prepopulated_fields = {"url_name": ("label",)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("label", "category", "subcategory", "price", "rarity")
    list_filter = ("category", "subcategory", "rarity")
    search_fields = ("label", "description", "element", "reality_fragment")


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("user__username", "item__label")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("item", "quantity", "price_at_purchase")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]