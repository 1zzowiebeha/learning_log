from django.urls import path

from . import views

app_name = "stats"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:topic_id>/', views.topic_data, name="topic_data")
]


# we will show the datapoint edit link from learning_logs here
# we will show a topic selection menu
# we will show statistics plots on a topic dashboard