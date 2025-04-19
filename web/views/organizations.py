from django.conf import settings
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from organizations.filters import OrganizationFilter
from organizations.models import Employee, Organization
from web.forms import OrganizationCreateForm

organization_queryset = Organization.objects.prefetch_related("employees").all()


class OrganizationListView(ListView):
    filterset_class = OrganizationFilter
    template_name = "organizations/list.html"
    paginate_by = settings.ORGANIZATION_PAGE_SIZE

    def get_queryset(self):
        return self.filterset_class(self.request.GET, organization_queryset, request=self.request).qs


class OrganizationDetailView(DetailView):
    queryset = organization_queryset
    template_name = "organizations/detail.html"


class OrganizationCreateView(CreateView):
    queryset = organization_queryset
    form_class = OrganizationCreateForm
    template_name = "organizations/create.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        Employee.objects.create(user=self.request.user, organization=self.object, is_admin=True, position="Создатель")
        return response


class OrganizationDeleteView(DeleteView):
    queryset = organization_queryset

    def get_success_url(self):
        return reverse("organization_list")
