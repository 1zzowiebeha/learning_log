"""Defines views for the learning_logs app."""

from django.http import HttpRequest, HttpResponse, Http404
from django.core.exceptions import BadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Model
from django.core.paginator import Paginator

from stats.helperutils import max_hours_reached, get_total_hours, max_length

from .models import Topic, Entry, TopicHourData
from .forms import TopicForm, EntryForm, TopicHoursDataForm


def check_owner(user: User, model: Model,
                owner_field: str = "owner"):
    """If the model is not owned by the user passed,
    raise a 404 error.
    
    owner_field is the User ForeignKey
    field on your model."""

    # TODO: Test this in the shell
    owner = getattr(model, owner_field)
    if user != owner:
        raise Http404


@require_GET
def index(request: HttpRequest):
    """The homepage for learning_logs."""
    return render(request, 'learning_logs/index.html')


@login_required
@require_GET
def topics(request: HttpRequest):
    """Show all topics."""
    
    topics = Topic.objects.filter(owner=request.user) \
                          .order_by("modified_on")
    paginator = Paginator(topics, 1)
    
    try:
        page_value = int(request.GET["page"])
    # first visit. no page requested
    except KeyError:
        page = paginator.page(1)
    # user manipulated page value
    except ValueError:
        raise BadRequest
    else:
        page = paginator.page(page_value)
        
    print(page.object_list)
              
    # user manipulated page value
    if page.number > paginator.num_pages:
        raise BadRequest
        
    context = {
        'page': page,
        'total_num_pages': paginator.num_pages,
        'inner_page_min': max(3, page.number),
    }
    
    return render(request, 'learning_logs/topics.html', context)


# TODO: class-based views might make these views more DRY (via inheritance),
#   since we repeat the same context/queries for multiple views.
@login_required
@require_GET
def topic(request: HttpRequest, topic_id: int):
    """Show a single topic and all its entries."""
    # Is it better to retrieve entries in the view, or the template?
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Make sure the topic belongs to the current user
    check_owner(request.user, topic)
    
    entries = topic.entry_set.order_by('-created_on')
    hours_form = TopicHoursDataForm(instance=topic,
                                    initial={'hours': 0})

    context = {
        "topic": topic,
        "entries": entries,
        "hours_create_form": hours_form,
        "total_hours": get_total_hours(topic),
        "max_hours_reached": max_hours_reached(topic),
    }

    return render(request, 'learning_logs/topic.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def new_topic(request: HttpRequest) -> HttpResponse:
    """Add a new topic."""
    if request.method == "POST":
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()

            return redirect('learning_logs:topics')
    else:
        # No data submitted; create a blank form.
        form = TopicForm()
        
    # Display a blank (GET) or invalid (invalid POST) form
    context = {
        'form': form,
    }
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Edit the given topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    
    check_owner(request.user, topic)
    
    if request.method == "POST":
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('learning_logs:topics')
    else:
        form = TopicForm(instance=topic)
        
    context = {
        'form': form,
        'topic': topic,
    }
    
    return render(request, 'learning_logs/edit_topic.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def delete_topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Delete the given topic."""
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=topic_id)
    
        check_owner(request.user, topic)
    
        topic.delete()
        
        return redirect('learning_logs:topics')
    else:
        raise BadRequest


@login_required
@require_http_methods(["GET", "POST"])
def new_entry(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Add a new entry for a given topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Make sure the topic belongs to the current user.
    check_owner(request.user, topic)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            
            return redirect("learning_logs:topic", topic_id=topic_id)
    else:
        form = EntryForm()
        
    context = {
        'form': form,
        'topic': topic
    }
    
    # Display a blank or invalid form.
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_entry(request: HttpRequest, entry_id: int) -> HttpRequest:
    """Edit page for the given entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    # Make sure the topic belongs to the current user.
    check_owner(request.user, topic) 

    if request.method == "POST":
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            
            return redirect('learning_logs:topic', topic_id=topic.id)
    else:
        form = EntryForm(instance=entry)
        
    context = {
        'form': form,
        'topic': topic,
        'entry': entry
    }
    
    # Display a blank or invalid form
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
@require_POST
def delete_entry(request: HttpRequest, entry_id: int) -> HttpRequest:
    """Delete the given entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    check_owner(request.user, topic)
    
    if request.method == "POST":
        entry.delete()
        
        return redirect('learning_logs:topic', topic_id=topic.id)
    else:
        raise BadRequest


@login_required
@require_http_methods(["GET", "POST"])
def edit_hours(request: HttpRequest, datapoint_id: int) -> HttpRequest:
    """Edit the given hour datapoint."""
    # Note: Repetition should be improved with CBVs.
    
    datapoint = get_object_or_404(TopicHourData, id=datapoint_id)
    topic = datapoint.topic
    
    check_owner(request.user, topic)
    
    if request.method == "POST":
        form = TopicHoursDataForm(instance=datapoint,
                                  data=request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('learning_logs:topic', topic_id=topic.id)
    else:
        form = TopicHoursDataForm(instance=datapoint)
        
    context = {
        "topic": topic,
        "datapoint": datapoint,
        "hours_edit_form": form,
        "total_hours": get_total_hours(topic),
        "max_hours_reached": max_hours_reached(topic),
    }
    
    return render(request, 'learning_logs/edit_hours.html', context)    
    
    
@login_required
@require_http_methods(["GET", "POST"])
def add_hours(request: HttpRequest, topic_id: int) -> HttpRequest:
    """Add a new datapoint for hours spent on a topic."""
    # Note: repetitive code is present here from the learning_logs:topic
    #   view. Class based views might make this more DRY.

    topic = get_object_or_404(Topic, id=topic_id)
    
    check_owner(request.user, topic)
    
    entries = topic.entry_set.order_by('-created_on')

    if request.method == "POST":
        form = TopicHoursDataForm(data=request.POST)
        if form.is_valid():
            datapoint = form.save(commit=False)
            data_entered = datapoint.hours
            
            total_hours = get_total_hours(topic)
            
            
            if "add" in request.POST:
                # User entered value that will bring
                #   total aggregated hours over field's max_length:
                if (total_hours + data_entered) > max_length:
                    hours_to_reach_max_length = max_length - total_hours
                    datapoint.hours = hours_to_reach_max_length
                # User entered a negative number:
                elif data_entered < 0:
                    # User entered a negative value that will bring us below 0:
                    if (total_hours + data_entered) < 0:
                        # Get negative total hours:
                        hours_to_reach_0 = total_hours * -1
                        datapoint.hours = hours_to_reach_0
                else:
                    datapoint.hours = data_entered
            elif "subtract" in request.POST:
                # User entered value that will bring total aggregated hours below 0:
                if (total_hours - data_entered) < 0:
                    # Get negative total hours:
                    hours_to_reach_0 = total_hours * -1
                    datapoint.hours = hours_to_reach_0
                # User entered a negative number (double negative)
                elif data_entered < 0:
                    # Addition would bring us over max_length:
                    if (total_hours - data_entered) > max_length:
                        hours_to_reach_max_length = max_length - total_hours
                        datapoint.hours = hours_to_reach_max_length
                    # Addition (negative * negative) is fine:
                    else:
                        datapoint.hours = (data_entered * -1)
                # User entered a valid positive number to subtract:
                else:
                    # Turn the positive number to subtract
                    #   into a negative for the db
                    datapoint.hours = (data_entered * -1)
            # No 'add', 'subtract' found in POST data
            else:
                raise BadRequest
            
            datapoint.topic = topic
            datapoint.save()
            
            return redirect('learning_logs:topic', topic_id=topic_id)
    else:
        form = TopicHoursDataForm()
        
    context = {
        "topic": topic,
        "entries": entries,
        "hours_create_form": form,
        "total_hours": get_total_hours(topic),
        "max_hours_reached": max_hours_reached(topic),
    }
    
    return render(request, 'learning_logs/topic.html', context)
