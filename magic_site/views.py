import random

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView

from api.models import Question
from magic_site.forms import AskQuestionForm, RegisterUserForm, LoginUserForm


def index(request):
    return render(request, template_name="index.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("login")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "login.html"
    extra_context = {"title": "Авторизация"}


@login_required
def ask_question(request):
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
        user = User.objects.get(pk=request.user.pk)
        form = AskQuestionForm()

        if request.method == "POST":
            question = request.POST.get("text")

            if not question:
                raise HttpResponseBadRequest
            Question.objects.create(
                user=user,
                text=question,
                answer=answer,
            )
            context = {"answer": answer, "form": form}
            return render(request, template_name="ask_question.html", context=context)

        context = {
            "form": form,
        }
        return render(request, template_name="ask_question.html", context=context)

    except Exception as e:
        return render(
            request, template_name="error.html", context={"error_message": str(e)}
        )


@login_required()
def get_history_questions(request):
    try:
        questions = (
            (
                Question.objects.select_related("user")
                .filter(user__pk=request.user.pk)
                .values("text")
                .annotate(total=Count("text"))
            )
            .values("user", "text", "answer", "total")

        )

        if not questions:
            raise HttpResponseNotFound

        data = {"questions": questions}

        return render(request, template_name="history_questions.html", context=data)
    except Exception as e:
        return render(
            request, template_name="error.html", context={"error_message": str(e)}
        )
