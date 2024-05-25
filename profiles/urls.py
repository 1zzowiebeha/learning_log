"""Defines URL patterns for profiles."""

from django.urls import path, include

from . import views

app_name = "profiles"
urlpatterns = [
    # If an authenticated user accesses the login page, redirect them
    # .. to the "next" GET query param, or to LOGIN_REDIRECT_URL if "next"
    # .. isn't supplied.
    #   path('login/', LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('<uuid:profile_uuid>/', views.profile, name="profile"),
    path('<uuid:profile_uuid>/add_friend/', views.add_friend, name="add_friend"),
    path('<uuid:profile_uuid>/friends/', views.view_friends, name="view_friends"),
    
    path('settings/', views.settings, name="settings"),
    path('settings/update_profile_settings/', views.update_profile_settings, name="update_profile_settings"),
]