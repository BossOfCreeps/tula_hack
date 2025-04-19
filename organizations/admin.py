from django.contrib import admin

from organizations.models import Employee, Organization


@admin.register(Organization)
class OrganisationAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
