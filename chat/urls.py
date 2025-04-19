from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chat.views import MessageViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r"message", MessageViewSet, basename="message")
router.register(r"notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
