"""Defines views for the accounts app."""

from typing import Any
from urllib.parse import urlencode

from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.conf import settings

from profiles.models import UserProfile

def redirect_after_login(request: HttpRequest):
    """Redirects to the value defined in the "next" query."""
    # Note: This is not in use yet.
    # Note: We can grab this POST data instead to have cleaner
    #   urls.
    
    # Can the user redirect themselves to resources like js files?
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=settings.SECURE_SSL_REDIRECT):

        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # Should I urlencode nxt?
        return redirect(nxt)
    
    
def login(request: HttpRequest):
    """A login page to provide user authentication."""
    # Note: This view is not in use yet.
    # TODO: Allow for case insensitive logins
    # TODO: If login credentials are incorrect, don't forget the
    #   "next" GET query.
    # Turn into a CBV in order to get redirect authenticated user functionality.
    
    if request.user.is_authenticated:
        raise HttpResponseBadRequest("You are already logged in.")

    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            
            try:
                profile = user.userprofile
            except AttributeError:
                # User is legacy user. Give them a user profile.
                new_profile = UserProfile.objects.create(user=user)
            
            auth_login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)
            #redirect_after_login(request)
    else:
        form = AuthenticationForm()
        
    context = {
        'form': form
    }
    
    return render(request, "registration/login.html", context)


def register(request: HttpRequest):
    """Register a new user account."""
    if request.user.is_authenticated:
        raise HttpResponseBadRequest("You are already logged in.")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = UserProfile.objects.create(user=new_user)
            
            auth_login(request, new_user)

            return redirect('learning_logs:index')
    else:
        form = UserCreationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)