from django.urls import path
from django.views.generic import TemplateView

from web.views import (
    CallCreateView,
    CallDeleteView,
    CallDetailView,
    CallListView,
    EmployeeCreateView,
    EmployeeDeleteView,
    LoginView,
    LogoutView,
    MatchCreateView,
    MatchDeleteView,
    MatchDetailView,
    MatchListView,
    MatchSucceedView,
    MessageCreateView,
    NotificationsSeedView,
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationDetailView,
    OrganizationListView,
    ProfileView,
    RegisterView,
    speech_to_text,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    #
    path("ajax/speech-to-text/", speech_to_text, name="speech_to_text"),
    #
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    #
    path("organizations/", OrganizationListView.as_view(), name="organization_list"),
    path("organizations/create/", OrganizationCreateView.as_view(), name="organization_create"),
    path("organizations/<int:pk>/", OrganizationDetailView.as_view(), name="organization_detail"),
    path("organizations/<int:pk>/delete/", OrganizationDeleteView.as_view(), name="organization_delete"),
    #
    path("employees/create/", EmployeeCreateView.as_view(), name="employee_create"),
    path("employees/<int:pk>/delete/", EmployeeDeleteView.as_view(), name="employee_delete"),
    #
    path("calls/", CallListView.as_view(), name="call_list"),
    path("calls/create/", CallCreateView.as_view(), name="call_create"),
    path("calls/<int:pk>/", CallDetailView.as_view(), name="call_detail"),
    path("calls/<int:pk>/delete/", CallDeleteView.as_view(), name="call_delete"),
    #
    path("matches/", MatchListView.as_view(), name="match_list"),
    path("matches/create/", MatchCreateView.as_view(), name="match_create"),
    path("matches/<int:pk>/", MatchDetailView.as_view(), name="match_detail"),
    path("matches/<int:pk>/delete/", MatchDeleteView.as_view(), name="match_delete"),
    path("matches/<int:pk>/succeed/", MatchSucceedView.as_view(), name="match_succeed"),
    #
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    #
    path("notifications/seed/", NotificationsSeedView.as_view(), name="notifications_seed"),
]
