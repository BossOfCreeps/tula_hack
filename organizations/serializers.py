from rest_framework import serializers

from organizations.models import Employee, Organization
from users.models import User
from users.serializers import UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user", write_only=True)

    class Meta:
        model = Employee
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)

    employees = EmployeeSerializer(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = "__all__"
