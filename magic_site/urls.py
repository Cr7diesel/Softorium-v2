from django.contrib.auth.views import LogoutView
from django.urls import path

from magic_site.views import (
    ask_question,
    get_history_questions,
    RegisterUser,
    LoginUser,
    index,
)

urlpatterns = [
    path("question/", ask_question, name="question"),
    path("history_questions/", get_history_questions, name="history_questions"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("", index, name="welcome"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
