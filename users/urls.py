from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from users.views import MeView, RegistrationView

urlpatterns = [
    path("reg/", RegistrationView.as_view(), name="reg"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
]
