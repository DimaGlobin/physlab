"""Views for the problems app."""
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import Topic


def topic_list(request):
    """Главная страница — список разделов физики."""
    topics = Topic.objects.annotate(problem_count=Count('problems'))
    return render(request, 'problems/topic_list.html', {'topics': topics})
