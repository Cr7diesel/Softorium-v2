from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'Вопрос: {self.text}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
