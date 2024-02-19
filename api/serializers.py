from rest_framework import serializers

from .models import Question


class AskQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class GetQuestionSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(default=None)

    class Meta:
        model = Question
        fields = "__all__"
