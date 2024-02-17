from django.urls import path

from api.views import AskQuestion, GetHistoryQuestions


urlpatterns = [
    path("ask_question/", AskQuestion.as_view(), name="ask_question"),
    path(
        "get_history_questions/",
        GetHistoryQuestions.as_view(),
        name="get_history_questions",
    ),
]
