from django import forms

from calls.models import Call, Match
from chat.models import Message
from organizations.models import Employee, Organization
from utils import HelpFormat, HelpType


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    city = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    help_types = forms.MultipleChoiceField(
        choices=HelpType.choices, widget=forms.CheckboxSelectMultiple, required=False
    )

    help_formats = forms.MultipleChoiceField(
        choices=HelpFormat.choices, widget=forms.CheckboxSelectMultiple, required=False
    )


class OrganizationCreateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


class CallCreateForm(forms.ModelForm):
    class Meta:
        model = Call
        exclude = ["status"]


class MatchCreateForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ["status"]


class MatchSucceedForm(forms.Form):
    text = forms.CharField(required=False)
    rating = forms.IntegerField()
    match = forms.ModelChoiceField(queryset=Match.objects.all())
    close = forms.IntegerField()


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
