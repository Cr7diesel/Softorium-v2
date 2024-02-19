from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from api.models import Question


class AskQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("text",)
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваш вопрос"}
            )
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "email": "E-mail",
        }
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-input"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]
