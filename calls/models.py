from django.db import models
from django.urls import reverse

from users.models import User
from utils import HelpFormat, HelpType


class CallStatus(models.TextChoices):
    NEW = "NEW", "Новая"
    IN_PROGRESS = "IN_PROGRESS", "В работе"
    DONE = "DONE", "Завершена"


class Call(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "calls")

    type = models.CharField("Тип помощи", choices=HelpType.choices, max_length=100)
    format = models.CharField("Формат помощи", choices=HelpFormat.choices, max_length=100)
    text = models.TextField("Описание")
    address = models.TextField("Адрес")
    contacts = models.TextField("Контакты")
    time = models.TextField("Время")

    status = models.CharField("Статус", choices=CallStatus.choices, max_length=100, default=CallStatus.NEW.value)

    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def __str__(self):
        return f"#{self.id} - {self.get_type_display()} ({self.get_format_display()})"

    def get_absolute_url(self):
        return reverse("call_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class MatchStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Активная"
    SUCCESS = "SUCCESS", "Успешная"
    CLOSED = "CLOSE", "Закрыта"


class Match(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "matches")
    call = models.ForeignKey(Call, models.CASCADE, "matches")

    rating = models.IntegerField("Рейтинг", default=None, null=True, blank=True)
    comment = models.TextField("Комментарий", null=True, blank=True)
    status = models.CharField("Статус", choices=MatchStatus.choices, max_length=100, default=MatchStatus.ACTIVE.value)

    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def set_rating(self, comment, rating, is_success):
        self.comment = comment
        self.rating = rating
        self.status = MatchStatus.SUCCESS.value if is_success else MatchStatus.CLOSED.value
        self.save()

        self.user.rating = Match.objects.filter(user=self.user).aggregate(models.Avg("rating"))["rating__avg"]
        self.user.save()

        if is_success:
            call: Call = self.call
            call.status = CallStatus.DONE
            call.save()

    def get_absolute_url(self):
        return reverse("match_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
