"""Views for the problems app."""
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm, FeedbackForm
from .models import Attempt, Feedback, Problem, Topic


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


def stats(request):
    """Страница статистики по всем попыткам."""
    total_attempts = Attempt.objects.count()
    correct_attempts = Attempt.objects.filter(is_correct=True).count()
    correct_percent = (
        round(correct_attempts / total_attempts * 100)
        if total_attempts > 0 else 0
    )

    topic_stats = []
    topics = Topic.objects.annotate(
        total=Count('problems__attempts'),
        correct=Count(
            'problems__attempts',
            filter=Q(problems__attempts__is_correct=True),
        ),
    ).filter(total__gt=0)

    for topic in topics:
        percent = round(topic.correct / topic.total * 100) if topic.total else 0
        topic_stats.append({
            'title': topic.title,
            'total': topic.total,
            'correct': topic.correct,
            'percent': percent,
        })

    return render(request, 'problems/stats.html', {
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'correct_percent': correct_percent,
        'topic_stats': topic_stats,
    })


def about(request):
    """Страница «О проекте» с формой обратной связи."""
    success = False

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message'],
            )
            success = True
            form = FeedbackForm()
    else:
        form = FeedbackForm()

    return render(request, 'problems/about.html', {
        'form': form,
        'success': success,
    })
