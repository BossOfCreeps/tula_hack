from django.db import models
from django.urls import reverse

from users.models import User


class Organization(models.Model):
    name = models.TextField(verbose_name="Название организации", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    logo = models.ImageField(upload_to="organization/", verbose_name="Логотип", blank=True, null=True)
    legal_name = models.TextField(verbose_name="Юридическое название", blank=True, null=True)
    tax_id = models.TextField(verbose_name="ИНН", blank=True, null=True)

    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    vk = models.URLField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.id])


class Employee(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "employees")
    organization = models.ForeignKey(Organization, models.CASCADE, "employees")
    position = models.TextField(verbose_name="Должность")
    is_admin = models.BooleanField(verbose_name="Админ организации", default=False)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
