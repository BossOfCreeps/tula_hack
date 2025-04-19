import django_filters
from django.db.models import Q

from organizations.models import Employee, Organization


class OrganizationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    my = django_filters.CharFilter(method="filter_my")

    @staticmethod
    def filter_search(queryset, _, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def filter_my(self, queryset, _, value):
        if value == "employee":
            return queryset.filter(id__in=Employee.objects.filter(user=self.request.user).values("organization_id"))
        if value == "admin":
            return queryset.filter(
                id__in=Employee.objects.filter(user=self.request.user, is_admin=True).values("organization_id")
            )
        return queryset

    class Meta:
        model = Organization
        fields = ["name"]


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = "__all__"
