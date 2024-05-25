from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from django.db.models import Subquery

from .models import UserProfile
from .forms import ProfileSettingsForm


@login_required
def view_friends(request: HttpRequest, profile_uuid: str):
    """View friends list for the given user profile."""
    requested_profile = get_object_or_404(UserProfile, uuid=profile_uuid)
    current_user_profile = request.user.userprofile
    
    is_current_user_a_friend = requested_profile.friends.filter(
        uuid=current_user_profile.uuid
    ).exists()
    
    friends_list = requested_profile.friends.all()
    
    context = {
        'friends_list': friends_list,
        'profile': requested_profile,
        'is_current_user_a_friend': is_current_user_a_friend,
    }
    
    return render(request, 'profiles/friends_list.html', context)


@login_required
def view_friend_requests(request: HttpRequest):
    """View all friend requests."""
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    friend_requests = current_user_profile.pending_friends.all()
    
    context = {
        'friend_requests': friend_requests,
    }
    
    return render(request, 'profiles/friend_requests.html', context)


@login_required
def request_friend(request: HttpRequest):
    """Add a friend to the user's pending friends list."""
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        try:
            friend_uuid = request.POST["profile_uuid"]
        except KeyError:
            # User manipulated the uuid: blank
            raise BadRequest
        else:
            # User manipulated the uuid: Can't send a friend request to yourself!
            if current_user_profile.uuid == friend_uuid:
                raise BadRequest
            else:
                friend_profile = get_object_or_404(UserProfile, uuid=friend_uuid)
                
                # User's profile is private. Their profile can't be seen.
                if not friend_profile.is_public:
                    raise BadRequest
                
                current_user_profile.pending_friends.add(friend_profile)
                
                return redirect("profiles:profile", profile_uuid=friend_uuid)
    else:
        raise BadRequest


@login_required
def remove_friend(request: HttpRequest):
    """Remove a friend from the user's friends list."""
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        try:
            friend_uuid = request.POST["profile_uuid"]
        except KeyError:
            # User manipulated the uuid: blank
            raise BadRequest
        else:
            # User manipulated the uuid: Can't unfriend yourself!
            if current_user_profile.uuid == friend_uuid:
                raise BadRequest
            else:
                friend_profile = get_object_or_404(UserProfile, uuid=friend_uuid)
                is_friends = current_user_profile.friends.filter(uuid=friend_profile.uuid).exists()
                if is_friends:
                    current_user_profile.friends.remove(friend_profile)
                # You aren't friends with this user!
                else:
                    raise BadRequest
                
                return redirect("profiles:profile", profile_uuid=friend_uuid)
    else:
        raise BadRequest
    
    
@login_required
def accept_friend(request: HttpRequest):
    """Accept a friend request."""
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        try:
            friend_request_uuid = request.POST["friend_request_uuid"]
        except KeyError:
            # User manipulated the uuid: blank
            raise BadRequest
        else:
            # User manipulated the uuid: Can't friend yourself!
            if current_user_profile.uuid == friend_request_uuid:
                raise BadRequest
            else:
                friend_profile = get_object_or_404(UserProfile, uuid=friend_request_uuid)
                
                current_user_profile.pending_friends.remove(friend_profile)
                current_user_profile.friends.add(friend_profile)
                
                return redirect("profiles:view_friend_requests")
    else:
        raise BadRequest
    
    
@login_required
def decline_friend(request: HttpRequest):
    """Decline a friend request."""
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        try:
            friend_request_uuid = request.POST["friend_request_uuid"]
        except KeyError:
            # User manipulated the uuid: blank
            raise BadRequest
        else:
            # User manipulated the uuid: Can't friend yourself!
            if current_user_profile.uuid == friend_request_uuid:
                raise BadRequest
            else:
                friend_profile = get_object_or_404(UserProfile, uuid=friend_request_uuid)
                
                current_user_profile.pending_friends.remove(friend_profile)
                
                return redirect("profiles:view_friend_requests")
    else:
        raise BadRequest
    
    
@login_required
def settings(request: HttpRequest):
    """UserProfile settings page."""
    # TODO: use CBVs
    
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    form = ProfileSettingsForm(instance=current_user_profile)
    
    context = {
        'form': form,
    }
    return render(request, 'profiles/settings.html', context)


@login_required
def update_profile_settings(request: HttpRequest):
    """Process the ProfileSettingsForm POST data,
    or return a ProfileSettingsForm for a GET request."""
    # Use CBVs to reduce repetition
    
    # for max security use s3 to separate media files from your code execution
    #   environment

    # should never 404, since the user is known to be authenticated
    #   via login_required.
    current_user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        
        form = ProfileSettingsForm(
            instance=current_user_profile,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            
            return redirect('profiles:settings')
    else:
        form = ProfileSettingsForm(
            instance=current_user_profile,
        )
        
    context = {
        'form': form
    }
    
    # invalid form, or a get request 
    return render(request, 'profiles/settings.html', context)
        #https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side


@login_required
def profile(request: HttpRequest, profile_uuid: str):
    """Display a userprofile."""
    requested_profile = get_object_or_404(UserProfile, uuid=profile_uuid)
    current_user_profile = request.user.userprofile
    
    is_current_user_a_friend = requested_profile.friends.filter(
        uuid=current_user_profile.uuid
    ).exists()
    
    is_friend_request_pending = requested_profile.pending_friends.filter(
        uuid=current_user_profile.uuid
    ).exists()
    
    context = {
        "profile": requested_profile,
        'is_current_user_a_friend': is_current_user_a_friend,
        'is_friend_request_pending': is_friend_request_pending,
    }
    
    return render(request, 'profiles/profile.html', context)