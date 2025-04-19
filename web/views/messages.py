from django.urls import reverse
from django.views.generic import CreateView

from chat.models import Message
from web.forms import MessageCreateForm


class MessageCreateView(CreateView):
    queryset = Message.objects.all()
    form_class = MessageCreateForm
    # template_name = "matches/create.html"

    def get_success_url(self):
        return reverse("match_detail", kwargs={"pk": self.object.match_id})
