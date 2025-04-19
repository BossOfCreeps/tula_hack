from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView

from calls.filters import MatchFilter
from calls.models import Match
from users.models import User
from web.forms import MatchCreateForm, MatchSucceedForm

match_queryset = Match.objects.select_related("user", "call__user").prefetch_related("messages").all()


class MatchListView(ListView):
    filterset_class = MatchFilter
    template_name = "matches/list.html"
    paginate_by = 3

    def get_queryset(self):
        return self.filterset_class(
            self.request.GET, match_queryset.filter(user=self.request.user), request=self.request
        ).qs

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs) | {"all_users": User.objects.all()}


class MatchDetailView(DetailView):
    queryset = match_queryset
    template_name = "matches/detail.html"


class MatchCreateView(CreateView):
    queryset = match_queryset
    form_class = MatchCreateForm
    template_name = "matches/create.html"


class MatchDeleteView(DeleteView):
    queryset = match_queryset

    def get_success_url(self):
        return reverse("match_list")


class MatchSucceedView(FormView):
    queryset = match_queryset
    form_class = MatchSucceedForm
    template_name = "matches/succeed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.queryset.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        data["match"].set_rating(data["text"], data["rating"], data["close"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("index")
