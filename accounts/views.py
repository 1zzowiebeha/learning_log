from typing import Any
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings
from urllib.parse import urlencode
from django.utils.http import url_has_allowed_host_and_scheme

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

# Create your views here.

def redirect_after_login(request: HttpRequest):
    # can the user redirect themselves to resources like js files?
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=settings.SECURE_SSL_REDIRECT):
        # redirect
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # should I urlencode nxt?
        return redirect(nxt)
    

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    redirect_field_name = 'next'

    def __init__(self, **kwargs: Any) -> None:
        self.redirect_authenticated_user = True
        self.redirect_field_name = 'next'

        super().__init__(**kwargs)
    
def login(request: HttpRequest):
    # if password is wrong, don't forget next query
    # allow for case insensitive usernames
    if request.user.is_authenticated:
        raise HttpResponseBadRequest("You are already logged in.")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                #user = form.save() # why do we have save if it isn't a modelform?
                auth_login(request, user)

                redirect_after_login(request)
        else:
            form = AuthenticationForm()
            
        context = {
            'form': form
        }
        
        return render(request, "accounts/login.html", context)


def register(request: HttpRequest):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth_login(request, new_user)

            return redirect('learning_logs:index')
    else:
        form = UserCreationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)