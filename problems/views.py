"""Views for the problems app."""
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm
from .models import Problem, Topic


def topic_list(request):
    """Главная страница — список разделов физики."""
    topics = Topic.objects.annotate(problem_count=Count('problems'))
    return render(request, 'problems/topic_list.html', {'topics': topics})


def problem_list(request, slug):
    """Список задач выбранного раздела."""
    topic = get_object_or_404(Topic, slug=slug)
    problems = topic.problems.all()
    return render(request, 'problems/problem_list.html', {
        'topic': topic,
        'problems': problems,
    })


def problem_detail(request, pk):
    """Карточка задачи с формой ответа."""
    problem = get_object_or_404(Problem, pk=pk)
    form = AnswerForm()
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'form': form,
    })
