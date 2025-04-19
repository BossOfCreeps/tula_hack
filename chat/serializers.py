from rest_framework import serializers

from chat.models import Message, Notification
from users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        return Message.objects.create(user=self.context["request"].user, **validated_data)

    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
