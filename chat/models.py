from django.db import models

from calls.models import Match
from users.models import User


class Message(models.Model):
    match = models.ForeignKey(Match, models.CASCADE, "messages")
    user = models.ForeignKey(User, models.CASCADE, "messages")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Notification(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "notifications")
    title = models.TextField(verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    link = models.URLField(verbose_name="Ссылка", null=True, blank=True)
    is_viewed = models.BooleanField(default=False, verbose_name="Просмотрено")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_and_send(cls, user, title, text, link):
        return Notification.objects.create(user=user, title=title, text=text, link=link)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
