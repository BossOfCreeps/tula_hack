from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, View

from calls.models import Call, Match
from organizations.models import Employee
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


class ProfileView(FormView):
    template_name = "users/profile.html"
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "calls": Call.objects.filter(user=self.request.user),
            "matches": Match.objects.filter(user=self.request.user),
            "employees": Employee.objects.filter(user=self.request.user),
        }

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.city = form.cleaned_data["city"]
        user.help_types = form.cleaned_data["help_types"]
        user.help_formats = form.cleaned_data["help_formats"]
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile")
