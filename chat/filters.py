import django_filters

from chat.models import Message, Notification


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = "__all__"


class NotificationFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = "__all__"
