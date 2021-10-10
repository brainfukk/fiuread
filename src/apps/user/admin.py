from django.contrib import admin

from .models import Event, UserPurse, UserUnitRelation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "message")
    list_display = ("user", "type", "message", "created_at")


@admin.register(UserPurse)
class UserPurseAdmin(admin.ModelAdmin):
    search_fields = ("id", "user__id", "points")
    list_display = ("user", "points")


@admin.register(UserUnitRelation)
class UserUnitRelationAdmin(admin.ModelAdmin):
    search_fields = ("user__id", "unit__id", "progress")
    list_display = ("user", "unit", "progress")
