from django.db.models import Q

from calls.models import Call
from chat.models import Notification
from users.models import User


def volunteer_selection_logic(obj: Call):
    # TODO: вынести в celery

    query = User.objects.filter(help_formats__contains=[obj.format], help_types__contains=[obj.type])
    query = query.filter(~Q(id=obj.user.id))
    for user in query:
        Notification.create_and_send(user=user, title="Новая заявка", text="lorem ipsum")
