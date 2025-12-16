from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("orders/<int:order_id>/", views.order_detail_view, name="order_detail"),

]
