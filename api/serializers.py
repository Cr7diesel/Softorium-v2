from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(default=None)

    class Meta:
        model = Question
        fields = "__all__"
