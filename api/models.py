from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255, default="")
    asked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
