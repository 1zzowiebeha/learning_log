"""Defines URL patterns for accounts."""

from django.urls import path, include
from django.contrib.auth.views import LoginView

from . import views

app_name = "accounts"
urlpatterns = [
    # If an authenticated user accesses the login page, redirect them
    # .. to the "next" GET query param, or to LOGIN_REDIRECT_URL if "next"
    # .. isn't supplied.
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('register/', views.register, name="register"),
    path('', include('django.contrib.auth.urls')),
]