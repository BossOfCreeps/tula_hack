from django.db import models


class HelpType(models.TextChoices):
    PSYCHO = "PSYCHO", "Психологическая"
    FINANCIAL = "FINANCIAL", "Материальная"
    VOLUNTEER = "VOLUNTEER", "Волонтерская"


class HelpFormat(models.TextChoices):
    ONLINE = "ONLINE", "Онлайн"
    OFFLINE = "OFFLINE", "Оффлайн"
