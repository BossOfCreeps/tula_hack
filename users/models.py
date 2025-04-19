from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils import HelpFormat, HelpType


class User(AbstractUser):
    help_types = ArrayField(models.CharField(max_length=30, choices=HelpType.choices), default=list)
    help_formats = ArrayField(models.CharField(max_length=30, choices=HelpFormat.choices), default=list)

    rating = models.IntegerField(default=0)

    # TODO: город
