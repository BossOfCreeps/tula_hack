from django.contrib import admin

from calls.models import Call, Match


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
