"""Views for the problems app."""
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm
from .models import Attempt, Problem, Topic


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
    """Карточка задачи с формой ответа. При POST — проверка и редирект."""
    problem = get_object_or_404(Problem, pk=pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['user_answer'].strip()
            is_correct = user_answer.lower() == problem.answer.lower()
            Attempt.objects.create(
                problem=problem,
                user_answer=user_answer,
                is_correct=is_correct,
            )
            return redirect('problems:problem_result', pk=problem.pk)
    else:
        form = AnswerForm()

    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'form': form,
    })


def problem_result(request, pk):
    """Результат последней попытки решения задачи."""
    problem = get_object_or_404(Problem, pk=pk)
    attempt = problem.attempts.order_by('-created_at').first()

    if attempt is None:
        return redirect('problems:problem_detail', pk=pk)

    return render(request, 'problems/problem_result.html', {
        'problem': problem,
        'is_correct': attempt.is_correct,
        'user_answer': attempt.user_answer,
    })
