"""Models for the problems app."""
from django.db import models


class Topic(models.Model):
    """Раздел физики (например, «Механика», «Оптика»)."""

    title = models.CharField('название', max_length=100)
    slug = models.SlugField('слаг', unique=True)
    description = models.TextField('описание', blank=True)
    order = models.PositiveIntegerField('порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'

    def __str__(self):
        return self.title


class Problem(models.Model):
    """Задача по физике."""

    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFFICULTY_CHOICES = [
        (EASY, 'Лёгкая'),
        (MEDIUM, 'Средняя'),
        (HARD, 'Сложная'),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='раздел',
    )
    title = models.CharField('название', max_length=200)
    text = models.TextField('условие')
    answer = models.CharField('правильный ответ', max_length=100)
    solution = models.TextField('разбор решения', blank=True)
    difficulty = models.CharField(
        'сложность',
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=EASY,
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self):
        return self.title


class Attempt(models.Model):
    """Попытка решения задачи."""

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='задача',
    )
    user_answer = models.CharField('ответ пользователя', max_length=100)
    is_correct = models.BooleanField('верно')
    created_at = models.DateTimeField('дата попытки', auto_now_add=True)

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f'{self.problem} — {status}'


class Feedback(models.Model):
    """Сообщение обратной связи."""

    name = models.CharField('имя', max_length=100)
    message = models.TextField('сообщение')
    created_at = models.DateTimeField('дата', auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return f'{self.name} — {self.created_at:%d.%m.%Y}'
