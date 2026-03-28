"""URL configuration for problems app."""
from django.urls import path

from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
]
