from django.contrib import admin
from django.db import models
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from .models import Unit, UnitExerciseElement, UnitTheoryElement, Topic, UnitExerciseElementAnswer
from .schema import UnitExerciseElementAnswerDataSchema


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ("id", "topic__name", "name")
    list_display = ("topic", "name")


@admin.register(UnitExerciseElement)
class UnitExerciseElementAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "content")
    list_display = ("unit", "type", "content")


@admin.register(UnitTheoryElement)
class UnitTheoryElementAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "content")
    list_display = ("unit", "type", "content")


@admin.register(UnitExerciseElementAnswer)
class UnitExerciseElementAnswerAdmin(admin.ModelAdmin):
    search_fields = ("id", "exercise__type", "exercise__unit")
    list_display = ("exercise", "data", "is_correct")
    raw_id_fields = ("exercise",)
