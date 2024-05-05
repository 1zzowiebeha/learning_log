"""Defines URL patterns for the learning_logs app."""

from django.urls import path

from . import views

app_name = "learning_logs"
urlpatterns = [
    path('', views.index, name="index"),
    # List page that shows all topics.
    path('topics/', views.topics, name="topics"),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name="topic"),
    # Page for adding a new topic.
    path('new_topic/', views.new_topic, name="new_topic"),
    # Page for editing a topic.
    path('edit_topic/<int:topic_id>/', views.edit_topic, name="edit_topic"),
    # Page for deleting a topic.
    path('delete_topic/<int:topic_id>/', views.delete_topic, name="delete_topic"),
    
    
    
    # Page for adding a new topic hour data point.
    path('add_hours/<int:topic_id>/', views.add_hours, name="add_hours"),
    # Page for editing a topic hour data point.
    path('edit_hours/<int:datapoint_id>/', views.edit_hours, name="edit_hours"),
    
    # Page for adding a new entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name="new_entry"),
    # Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name="edit_entry"),
    # Page for deleting an entry.
    path('delete_entry/<int:entry_id>/', views.delete_entry, name="delete_entry"),
]