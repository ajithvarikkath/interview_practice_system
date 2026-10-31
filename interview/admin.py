from django.contrib import admin
from .models import Category, Question, InterviewSession, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question_text",
        "category",
        "difficulty",
    )


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "started_at",
        "completed",
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "interview",
        "question",
        "ai_score",
        "created_at",
    )