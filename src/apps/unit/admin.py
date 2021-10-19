from django.contrib import admin

from .models import (
    Unit,
    UnitExerciseElement,
    UnitTheoryElement,
    Topic,
    UnitExerciseElementAnswer,
    UnitUserAnswer
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ("id", "topic__name", "name")
    list_display = ("topic", "name")
    raw_id_fields = ("topic",)

    def save_model(self, request, obj, form, change):
        unit = None
        if hasattr(obj, "id"):
            try:
                unit = Unit.objects.get(id=obj.id)
            except Unit.DoesNotExist:  # noqa
                unit = None

        if unit is None:
            return Unit.objects.create_unit(
                topic=obj.topic,
                name=obj.name,
                desc=obj.description
            )
        return obj.save()


@admin.register(UnitExerciseElement)
class UnitExerciseElementAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "content")
    list_display = ("unit", "type", "content")
    raw_id_fields = ("unit",)


@admin.register(UnitTheoryElement)
class UnitTheoryElementAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "content")
    list_display = ("unit", "type", "content", "image", "order_number")
    raw_id_fields = ("unit",)


@admin.register(UnitExerciseElementAnswer)
class UnitExerciseElementAnswerAdmin(admin.ModelAdmin):
    search_fields = ("id", "exercise__type", "exercise__unit")
    list_display = ("exercise", "data", "is_correct")
    raw_id_fields = ("exercise",)


@admin.register(UnitUserAnswer)
class UnitUserAnswerAdmin(admin.ModelAdmin):
    search_fields = ("unit__id", "exercise__id")
    list_display = ("unit", "exercise", "answer")
    raw_id_fields = ("unit", "exercise", "answer", "user")
