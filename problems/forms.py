"""Forms for the problems app."""
from django import forms


class AnswerForm(forms.Form):
    """Форма для ввода ответа на задачу."""

    user_answer = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Введите ответ.',
            'max_length': 'Ответ слишком длинный (максимум 100 символов).',
        },
    )
