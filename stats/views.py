from typing import List
from decimal import Decimal

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet

import plotly.offline as opy
import plotly.graph_objs as go


from learning_logs.models import Topic

from .helperutils import get_total_hours
# Create your vour views here.

# Next steps for this app:
# guarantee safety
# get my own static css to style the chart div a bit more
#// style the statistics link to be next to topics
#// topic edit / delete
#// entry delete
# do the book to completion
# take the plotly mastery course
# add the topic specific data visualization
# add ability to edit certain datapoints from a
# .. paginated list of all datapoints
#// turn the plots into offline plots
#   //(plotly 4+ is offline-only. online is a separate package now.)
# add profiles that show github-like visualization of data

# S3 uploads
# more about deployment
# become an expert at making some random app and deploying it
# tls, domain

# Beyond this app:
# odin project for frontend
# bootstrap docs for frontend

# for the browser to cache javascript,
# .. and to allow the plot to work with a
# .. Content Security Policy that disables inline JS,
# .. use the JS plotly library and use Data Attributes.
# (download the js and put into static directory,
#  pass stuff to the plots)
#  make the plots with javascript

# also download bootstrap css/js so the browser can cache it.
# right now, if I lose internet, I lose bootstrap too.
# .. for some reason. idk why

# question: why do we redirect after post?

# regular forms documentation
# models documentation / codeacademy vids
# CBV documentation / codeacademy vids
# auth project from tech with tim (requires CBV knowledge)
# auth CBVs and documentation
# testing from codecademy
# projects along the way
# pretty printed api app
    # deploy with env variables
# Django Rest Framework (ooooOO!!)
# Flask apps

def get_all_plot_data(topics: QuerySet) -> str:
    """Aggregates all topic data into a format
    that can easily be given to a plotly plot."""
    labels = []
    values = []
    for topic in topics:
        topic_hours = get_total_hours(topic)
        labels.append(topic.content)
        values.append(topic_hours)
        
    return (labels, values)

def generate_plot_html(labels: List[str], values: List[Decimal]):
    """Generate a plot and return it as an
    HTML string to embed into a page.""" 
    
    # don't render a plot if there is no data
    if all([value == 0 for value in values]) :
        return ""
     
    data = go.Pie(labels=labels, values=values, hole=0.3)
    layout = go.Layout(
        title="Total hours spent with each learning topic:",
    )
    figure = go.Figure(
        data=data,
        layout=layout
    )

    return figure.to_html(full_html=False,
                          default_height=500,
                          default_width=500)

@login_required
def index(request: HttpRequest) -> HttpResponse:
    # paginate
    topics = Topic.objects.filter(owner=request.user)
    context = {
        'topics': topics
    }
    
    plot_data = get_all_plot_data(topics)
    plot_html = generate_plot_html(plot_data[0], plot_data[1])
    
    context["topics_plot"] = plot_html
    
    return render(request, 'stats/index.html', context)

def topic_data(request: HttpRequest, topic_id: int) -> HttpResponse:
    return render(request, 'stats/coming_soon.html')

# def edit_hours_datapoint(request: HttpRequest, topic_id: int) -> HttpResponse:
#     """Edit an hours datapoint."""
#     pass