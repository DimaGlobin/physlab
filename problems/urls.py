"""URL configuration for problems app."""
from django.urls import path

from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topics/<slug:slug>/', views.problem_list, name='problem_list'),
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problems/<int:pk>/result/', views.problem_result, name='problem_result'),
]
