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

    @extend_schema(description='ask the question',
                   operation_id='ask the question',
                   request=inline_serializer(
                       name='ask the question',
                       fields={
                           'question': s.CharField(),
                       }
                   ),
                   responses={
                       201: OpenApiResponse(description="Вопрос: текст вопроса, Ответ: текст ответа"),
                       400: OpenApiResponse(description='No question'),
                       401: OpenApiResponse(description='Incorrect authentication credentials.'),
                       403: OpenApiResponse(description="Credentials weren't provided"),
                       404: OpenApiResponse(description='Question does not exist'),
                   }
                   )
    def post(self, request):
        try:
            CHOICES = (
                "Да", "Нет", "Возможно", "Вопрос не ясен",
                "Абсолютно точно", "Никогда", "Даже не думай",
                "Сконцентрируйся и спроси опять"
            )
            answer = random.choice(CHOICES)
            question_request = request.data.get('question')
            user = request.user
            if not question_request:
                return Response({'Ошибка': 'Нужно задать вопрос'}, status=status.HTTP_400_BAD_REQUEST)

            question = Question.objects.create(user=user, text=question_request)
            return Response({'Вопрос': question.text, 'Ответ': answer}, status=status.HTTP_201_CREATED)
        except exceptions.PermissionDenied:
            return Response({'Ошибка': 'Недосточно прав'}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'Ошибка': 'вопросов нет'}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.AuthenticationFailed:
            return Response({'Ошибка': 'ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)


class GetHistoryQuestions(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(description='Get history questions',
                   operation_id='Get history questions',
                   responses={
                       (200, 'application/json'): OpenApiResponse(response=QuestionSerializer,
                                                                  description='Success'),
                       204: OpenApiResponse(description="You haven't any questions yet"),
                       401: OpenApiResponse(description='Incorrect authentication credentials.'),
                       403: OpenApiResponse(description="Credentials weren't provided"),
                       404: OpenApiResponse(description='Question does not exist'),
                   }
                   )
    def get(self, request):
        try:
            user = request.user
            questions = Question.objects.select_related(
                'user').filter(user=user).annotate(total=Count('question')).values('question', 'total')
            if not questions:
                return Response({'Извините': 'Вы не задали ни один вопрос'}, status=status.HTTP_204_NO_CONTENT)
            serializer = QuestionSerializer(data=questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except exceptions.PermissionDenied:
            return Response({'Ошибка': 'Недосточно прав'}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'Ошибка': 'вопросов нет'}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.AuthenticationFailed:
            return Response({'Ошибка': 'ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)


class GetAllHistoryQuestions(APIView):

    @extend_schema(description='Get all History questions',
                   operation_id='get all history questions',
                   responses={
                       (200, 'application/json'): OpenApiResponse(response=QuestionSerializer,
                                                                  description='Success'),
                       204: OpenApiResponse(description="You haven't any questions yet"),
                       401: OpenApiResponse(description='Incorrect authentication credentials.'),
                       404: OpenApiResponse(description='Question does not exist'),
                   }
                   )
    def get(self, request):
        try:
            questions = Question.objects.select_related(
                'user').all().annotate(total=Count('question')).values('question', 'total')
            if not questions:
                return Response({'Извините': 'нет вопросов'}, status=status.HTTP_204_NO_CONTENT)
            serializer = QuestionSerializer(data=questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'Ошибка': 'вопросов нет'}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.AuthenticationFailed:
            return Response({'Ошибка': 'ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)
