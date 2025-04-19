from django.urls import include, path
from rest_framework.routers import DefaultRouter

from calls.views import CallViewSet, MatchViewSet

router = DefaultRouter()
router.register(r"call", CallViewSet, basename="call")
router.register(r"match", MatchViewSet, basename="match")

urlpatterns = [
    path("", include(router.urls)),
]
