from django import forms
from django.contrib.auth.models import User
from core.models import Item, Category, SubCategory 

class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class UserSiteAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_active", "is_staff"]
