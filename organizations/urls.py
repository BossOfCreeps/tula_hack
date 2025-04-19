from django.urls import include, path
from rest_framework.routers import DefaultRouter

from organizations.views import EmployeeViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r"organization", OrganizationViewSet, basename="organization")
router.register(r"employee", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
]
