from django.contrib import admin

from chat.models import Message, Notification

admin.site.register(Message)
admin.site.register(Notification)
