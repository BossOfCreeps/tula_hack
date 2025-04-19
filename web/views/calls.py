from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View

from calls.filters import CallFilter
from calls.models import Call
from chat.models import Notification
from utils.volunteer_selection import volunteer_selection_logic
from web.forms import CallCreateForm

call_queryset = Call.objects.select_related("user").all()


class CallListView(ListView):
    filterset_class = CallFilter
    template_name = "calls/list.html"
    paginate_by = settings.CALL_PAGE_SIZE

    def get_queryset(self):
        return self.filterset_class(self.request.GET, call_queryset, request=self.request).qs


class CallDetailView(DetailView):
    queryset = call_queryset
    template_name = "calls/detail.html"


class CallCreateView(CreateView):
    queryset = call_queryset
    form_class = CallCreateForm
    template_name = "calls/create.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        volunteer_selection_logic(self.object)
        return response


class CallDeleteView(DeleteView):
    queryset = call_queryset

    def get_success_url(self):
        return reverse("call_list")


class NotificationsSeedView(View):
    def get(self, request):
        Notification.objects.filter(user=request.user).update(is_viewed=True)
        return redirect(self.request.GET.get("next", "/"))
