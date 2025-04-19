import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from calls.models import Match
from chat.models import Message, Notification


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.room_group_name = f"chat_{self.match_id}"

        # Проверка авторизации
        if self.scope["user"] == AnonymousUser():
            await self.close()
            return

        # Присоединяемся к группе комнаты
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)["message"]
        user_id = self.scope["user"].id

        # Сохраняем сообщение в БД
        new_message = await Message.objects.acreate(match_id=self.match_id, user_id=user_id, text=message)

        match = await Match.objects.select_related("call").aget(pk=self.match_id)
        await Notification.acreate_and_send(
            user_id=match.call.user_id if match.user_id == user_id else match.user_id,
            title="Новое сообщение в чате",
            text=message,
            link=reverse("match_detail", args=[self.match_id]),
        )

        # Отправляем сообщение в группу комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_id": user_id,
                "user_name": self.scope["user"].get_full_name() or self.scope["user"].username,
                "created_at": new_message.created_at.strftime("%H:%M"),
                "is_me": False,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user_id": event["user_id"],
                    "user_name": event["user_name"],
                    "created_at": event["created_at"],
                    "is_me": event["user_id"] == self.scope["user"].id,
                }
            )
        )
