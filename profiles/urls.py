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
    
    path('<uuid:profile_uuid>/friends/', views.view_friends, name="view_friends"),
    path('request_friend/', views.request_friend, name="request_friend"),
    path('remove_friend/', views.remove_friend, name="remove_friend"),
    
    path('pending_friends/', views.view_friend_requests, name="view_friend_requests"),
    path('accept_friend/', views.accept_friend, name="accept_friend"),
    path('decline_friend/', views.decline_friend, name="decline_friend"),
    
    path('settings/', views.settings, name="settings"),
    path('settings/update_profile_settings/', views.update_profile_settings, name="update_profile_settings"),
]