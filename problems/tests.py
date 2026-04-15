"""Tests for the problems app."""
from django.test import TestCase
from django.urls import reverse

from .models import Attempt, Feedback, Problem, Topic


class TopicModelTest(TestCase):
    """Tests for the Topic model."""

    def setUp(self):
        self.topic = Topic.objects.create(
            title='Механика', slug='mechanics',
        )

    def test_str(self):
        self.assertEqual(str(self.topic), 'Механика')


class ProblemModelTest(TestCase):
    """Tests for the Problem model."""

    def setUp(self):
        self.topic = Topic.objects.create(
            title='Оптика', slug='optics',
        )
        self.problem = Problem.objects.create(
            topic=self.topic, title='Линза',
            text='Найдите фокус', answer='10 см',
        )

    def test_str(self):
        self.assertEqual(str(self.problem), 'Линза')


class AttemptModelTest(TestCase):
    """Tests for the Attempt model."""

    def setUp(self):
        topic = Topic.objects.create(title='Механика', slug='mech')
        self.problem = Problem.objects.create(
            topic=topic, title='Задача', text='Условие', answer='42',
        )

    def test_str_correct(self):
        attempt = Attempt.objects.create(
            problem=self.problem, user_answer='42', is_correct=True,
        )
        self.assertIn('✓', str(attempt))

    def test_str_incorrect(self):
        attempt = Attempt.objects.create(
            problem=self.problem, user_answer='0', is_correct=False,
        )
        self.assertIn('✗', str(attempt))


class TopicListViewTest(TestCase):
    """Tests for the topic list page."""

    def setUp(self):
        Topic.objects.create(title='Механика', slug='mechanics')

    def test_status_code(self):
        response = self.client.get(reverse('problems:topic_list'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('problems:topic_list'))
        self.assertTemplateUsed(response, 'problems/topic_list.html')

    def test_contains_topic(self):
        response = self.client.get(reverse('problems:topic_list'))
        self.assertContains(response, 'Механика')


class ProblemListViewTest(TestCase):
    """Tests for the problem list page."""

    def setUp(self):
        self.topic = Topic.objects.create(title='Оптика', slug='optics')
        Problem.objects.create(
            topic=self.topic, title='Линза',
            text='Условие', answer='10',
        )

    def test_status_code(self):
        response = self.client.get(
            reverse('problems:problem_list', args=[self.topic.slug]),
        )
        self.assertEqual(response.status_code, 200)

    def test_contains_problem(self):
        response = self.client.get(
            reverse('problems:problem_list', args=[self.topic.slug]),
        )
        self.assertContains(response, 'Линза')


class ProblemDetailViewTest(TestCase):
    """Tests for the problem detail page and answer submission."""

    def setUp(self):
        topic = Topic.objects.create(title='Механика', slug='mech')
        self.problem = Problem.objects.create(
            topic=topic, title='Задача',
            text='Условие', answer='42',
        )

    def test_get(self):
        response = self.client.get(
            reverse('problems:problem_detail', args=[self.problem.pk]),
        )
        self.assertEqual(response.status_code, 200)

    def test_correct_answer(self):
        response = self.client.post(
            reverse('problems:problem_detail', args=[self.problem.pk]),
            {'user_answer': '42'},
        )
        self.assertRedirects(
            response,
            reverse('problems:problem_result', args=[self.problem.pk]),
        )
        attempt = Attempt.objects.first()
        self.assertTrue(attempt.is_correct)

    def test_incorrect_answer(self):
        self.client.post(
            reverse('problems:problem_detail', args=[self.problem.pk]),
            {'user_answer': 'wrong'},
        )
        attempt = Attempt.objects.first()
        self.assertFalse(attempt.is_correct)

    def test_case_insensitive(self):
        self.client.post(
            reverse('problems:problem_detail', args=[self.problem.pk]),
            {'user_answer': '42'},
        )
        attempt = Attempt.objects.first()
        self.assertTrue(attempt.is_correct)

    def test_empty_answer_rejected(self):
        response = self.client.post(
            reverse('problems:problem_detail', args=[self.problem.pk]),
            {'user_answer': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Attempt.objects.count(), 0)


class StatsViewTest(TestCase):
    """Tests for the statistics page."""

    def test_empty_stats(self):
        response = self.client.get(reverse('problems:stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_attempts'], 0)

    def test_stats_with_attempts(self):
        topic = Topic.objects.create(title='Механика', slug='mech')
        problem = Problem.objects.create(
            topic=topic, title='Задача', text='Условие', answer='42',
        )
        Attempt.objects.create(
            problem=problem, user_answer='42', is_correct=True,
        )
        Attempt.objects.create(
            problem=problem, user_answer='0', is_correct=False,
        )
        response = self.client.get(reverse('problems:stats'))
        self.assertEqual(response.context['total_attempts'], 2)
        self.assertEqual(response.context['correct_attempts'], 1)
        self.assertEqual(response.context['correct_percent'], 50)


class AboutViewTest(TestCase):
    """Tests for the about page and feedback form."""

    def test_get(self):
        response = self.client.get(reverse('problems:about'))
        self.assertEqual(response.status_code, 200)

    def test_valid_feedback(self):
        response = self.client.post(reverse('problems:about'), {
            'name': 'Иван',
            'message': 'Отличный проект, спасибо!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_short_message_rejected(self):
        self.client.post(reverse('problems:about'), {
            'name': 'Иван',
            'message': 'Ок',
        })
        self.assertEqual(Feedback.objects.count(), 0)
