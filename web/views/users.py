from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import FormView, View

from users.models import User
from web.forms import LoginForm, RegisterForm


class LoginView(FormView):
    form_class = LoginForm

    def form_valid(self, form):
        user = User.objects.filter(username=form.cleaned_data["username"]).first()
        if user and user.check_password(form.cleaned_data["password"]):
            login(self.request, user)
            return redirect(self.request.GET.get("next", "/"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(self.request.GET.get("next", "/"))


class RegisterView(FormView):
    form_class = RegisterForm

    def form_valid(self, form):
        user = User.objects.create(**form.cleaned_data)
        user.set_password(form.cleaned_data["password"])
        user.save()
        user.refresh_from_db()

        login(self.request, user)
        return redirect(self.request.GET.get("next", "/"))
