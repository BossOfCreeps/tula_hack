from django.db.models import Avg, Q
from django.urls import reverse

from calls.models import Call
from chat.models import Notification
from users.models import User
from utils import HelpFormat


def volunteer_selection_logic(obj: Call):
    # TODO: вынести в celery

    users = User.objects.filter(help_formats__contains=[obj.format], help_types__contains=[obj.type])
    users = users.filter(~Q(id=obj.user.id))

    if obj.format == HelpFormat.OFFLINE.value:
        users = users.filter(city=obj.user.city)

    wanted_rating = users.aggregate(Avg("rating"))["rating__avg"]
    users = users.filter(rating__gte=wanted_rating)

    for user in users:
        Notification.create_and_send(
            user=user,
            title="Новая заявка",
            text=f'Появилась заявка "{obj}"',
            link=reverse("call_detail", args=[obj.id]),
        )
