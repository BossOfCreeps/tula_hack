from django.db.models import Q
from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from organizations.models import Employee
from users.models import User
from web.forms import EmployeeCreateForm


class EmployeeCreateView(CreateView):
    queryset = Employee.objects.all()
    form_class = EmployeeCreateForm
    template_name = "employee/create.html"

    def get_context_data(self, **kwargs):
        ids = Employee.objects.filter(organization_id=self.request.GET["organization"]).values_list("user", flat=True)
        return {"available_users": User.objects.filter(~Q(id__in=ids))}

    def get_success_url(self):
        return reverse("organization_detail", kwargs={"pk": self.request.GET["organization"]})


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "employee/confirm_delete.html"
    organization_id = None

    def form_valid(self, form):
        self.organization_id = self.get_object().organization_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("organization_detail", kwargs={"pk": self.organization_id})
