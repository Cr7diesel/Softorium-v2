import random

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions, status, serializers as s

from .serializers import QuestionSerializer
from .models import Question


class AskQuestion(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Ask the question",
        operation_id="Ask the question",
        request=inline_serializer(
            name="Ask the question",
            fields={
                "question": s.CharField(),
            },
        ),
        responses={
            201: OpenApiResponse(
                description="Вопрос: текст вопроса, Ответ: текст ответа"
            ),
            400: OpenApiResponse(description="No question"),
            401: OpenApiResponse(description="Incorrect authentication credentials."),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description="Question does not exist"),
        },
    )
    def post(self, request):
        try:
            CHOICES = (
                "Да",
                "Нет",
                "Возможно",
                "Вопрос не ясен",
                "Абсолютно точно",
                "Никогда",
                "Даже не думай",
                "Сконцентрируйся и спроси опять",
            )

            answer = random.choice(CHOICES)
            question_request = request.data.get("question")
            user = request.user

            if not question_request:
                return Response(
                    {"Error": "Need to ask the question"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = {"user": user, "text": question_request, "answer": answer}

            serializer = QuestionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except exceptions.PermissionDenied:
            return Response(
                {"Error": "Permissions denied"}, status=status.HTTP_403_FORBIDDEN
            )
        except ObjectDoesNotExist:
            return Response(
                {"Error": "You're haven't any questions yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except exceptions.AuthenticationFailed:
            return Response(
                {"Error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )


class GetHistoryQuestions(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Get history questions",
        operation_id="get_history_questions",
        responses={
            (200, "application/json"): OpenApiResponse(
                response=QuestionSerializer, description="Success"
            ),
            204: OpenApiResponse(description="You haven't any questions yet"),
            401: OpenApiResponse(description="Incorrect authentication credentials."),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description="Question does not exist"),
        },
    )
    def get(self, request):
        try:
            questions = (
                Question.objects.select_related("user")
                .filter(user__pk=request.user.pk)
                .values("text")
                .annotate(total=Count("text"))
            ).values("user", "text", "total")

            if not questions:
                return Response(
                    {"Sorry": "You're don't ask the question"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            serializer = QuestionSerializer(data=list(questions), many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except exceptions.PermissionDenied:
            return Response(
                {"Error": "Permissions denied"}, status=status.HTTP_403_FORBIDDEN
            )
        except ObjectDoesNotExist:
            return Response(
                {"Error": "You're haven't any questions yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except exceptions.AuthenticationFailed:
            return Response(
                {"Error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )
