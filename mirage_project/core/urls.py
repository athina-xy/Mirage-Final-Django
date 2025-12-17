from django.urls import path
from . import views

urlpatterns = [
    path("manage/", views.admin_panel, name="admin_panel"),

    path("manage/items/", views.admin_items_list, name="admin_items_list"),
    path("manage/items/new/", views.admin_item_create, name="admin_item_create"),
    path("manage/items/<int:item_id>/edit/", views.admin_item_edit, name="admin_item_edit"),
    path("manage/items/<int:item_id>/delete/", views.admin_item_delete, name="admin_item_delete"),

    path("manage/categories/", views.admin_categories_list, name="admin_categories_list"),
    path("manage/categories/new/", views.admin_category_create, name="admin_category_create"),
    path("manage/categories/<int:category_id>/edit/", views.admin_category_edit, name="admin_category_edit"),
    path("manage/categories/<int:category_id>/delete/", views.admin_category_delete, name="admin_category_delete"),

    path("manage/users/", views.admin_users_list, name="admin_users_list"),
    path("manage/users/<int:user_id>/edit/", views.admin_user_edit, name="admin_user_edit"),
]
