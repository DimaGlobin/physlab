"""Admin configuration for the problems app."""
from django.contrib import admin

from .models import Attempt, Feedback, Problem, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin for Topic model."""

    list_display = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """Admin for Problem model."""

    list_display = ('title', 'topic', 'difficulty')
    list_filter = ('topic', 'difficulty')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """Admin for Attempt model."""

    list_display = ('problem', 'user_answer', 'is_correct', 'created_at')
    list_filter = ('is_correct',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin for Feedback model."""

    list_display = ('name', 'created_at')
