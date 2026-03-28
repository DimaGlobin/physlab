"""Forms for the problems app."""
from django import forms
from django.core.validators import MinLengthValidator


class AnswerForm(forms.Form):
    """Форма для ввода ответа на задачу."""

    user_answer = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Введите ответ.',
            'max_length': 'Ответ слишком длинный (максимум 100 символов).',
        },
    )


class FeedbackForm(forms.Form):
    """Форма обратной связи."""

    name = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Введите ваше имя.',
            'max_length': 'Имя слишком длинное (максимум 100 символов).',
        },
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        validators=[
            MinLengthValidator(10, 'Сообщение слишком короткое (минимум 10 символов).'),
        ],
        error_messages={
            'required': 'Введите сообщение.',
        },
    )
