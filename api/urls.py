from django.urls import path

from api.views import AskQuestion, GetHistoryQuestions, GetAllHistoryQuestions




urlpatterns = [
    path('ask_question/', AskQuestion.as_view(), name='ask_question'),
    path('get_history_questions/', GetHistoryQuestions.as_view(), name='get_history_questions'),
    path('get_all_history_questions/', GetAllHistoryQuestions.as_view(), name='get_all_history_questions')
]
