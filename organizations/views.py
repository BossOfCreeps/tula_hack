from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from organizations.filters import EmployeeFilter, OrganizationFilter
from organizations.models import Employee, Organization
from organizations.serializers import EmployeeSerializer, OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.prefetch_related("employees__user").all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        organization = serializer.save()
        Employee.objects.create(user=self.request.user, organization=organization, is_admin=True, position="Создатель")


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.select_related("user").all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
