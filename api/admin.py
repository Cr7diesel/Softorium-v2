from django.contrib import admin

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "answer", "asked_at")
    list_filter = ("id", "user", "answer", "asked_at")
