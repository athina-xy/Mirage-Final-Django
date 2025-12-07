from django.contrib import admin
from .models import Category, SubCategory, Item

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
