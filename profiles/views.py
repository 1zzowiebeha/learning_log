from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import ProfileImageForm


@login_required
def settings(request: HttpRequest):
    # use CBVs
    form = ProfileImageForm
    context = {
        'form': form
    }
    return render(request, 'profiles/settings.html', context)


@login_required
def upload_profile_image(request: HttpRequest):
    
    # Use CBVs to reduce repetition
    
    # for max security use s3 to separate media files from your code execution
    #   environment

    if request.method == "POST":
        # should never 404, since the user is authenticated.
        profile = get_object_or_404(UserProfile, user=request.user)
        
        form = ProfileImageForm(
            instance=request.user.userprofile,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            
            return redirect('profiles:upload_profile_image')
    else:
        form = ProfileImageForm(
            instance=request.user.userprofile,
        )
        
    context = {
        'form': form
    }
    
    # invalid form / get
    return render(request, 'profiles/settings.html', context)
        #https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side

@login_required
def profile(request: HttpRequest, profile_uuid: str):
    """Display a userprofile."""
    profile = get_object_or_404(UserProfile, uuid=profile_uuid)
    
    context = {
        "profile": profile
    }
    
    return render(request, 'profiles/profile.html', context)