"""Defines URL patterns for profiles."""

from django.urls import path, include

from . import views

app_name = "profiles"
urlpatterns = [
    # If an authenticated user accesses the login page, redirect them
    # .. to the "next" GET query param, or to LOGIN_REDIRECT_URL if "next"
    # .. isn't supplied.
    #   path('login/', LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('<int:profile_id>/', views.profile, name="profile"),
    path('settings/', views.settings, name="settings"),
    path('settings/upload_profile_image/', views.upload_profile_image, name="upload_profile_image"),
]