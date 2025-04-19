from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from chat.filters import MessageFilter, NotificationFilter
from chat.models import Message, Notification
from chat.serializers import MessageSerializer, NotificationSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.select_related("user", "match__call").all()
    serializer_class = MessageSerializer
    filterset_class = MessageFilter


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
