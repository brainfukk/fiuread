from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.utils.models import CommonModel
from src.apps.user.models import UserUnitRelation


class UnitManager(models.Manager):
    def create_users_unit_relation(self, unit, users):
        data = [
            UserUnitRelation(user=user, unit=unit)
            for user
            in users
        ]
        return UserUnitRelation.objects.bulk_create(data)

    def create_unit(self, topic, name, users):
        unit = Unit.objects.create(topic=topic, name=name)
        self.create_users_unit_relation(unit=unit, users=users)
        return unit


class UnitTheoryElementType(models.TextChoices):
    LIST_VIEW = "LIST_VIEW"

    PLAIN_TEXT_VIEW = "PLAIN_TEXT_VIEW"

    IMAGE_VIEW = "IMAGE_VIEW"
    IMAGE_LEFT_TEXT_VIEW = "IMAGE_LEFT_TEXT_VIEW"
    IMAGE_RIGHT_TEXT_VIEW = "IMAGE_RIGHT_TEXT_VIEW"


class UnitExerciseElementType(models.TextChoices):
    SELECT_VIEW = "SELECT_VIEW"
    TRUE_OR_FALSE_VIEW = "TRUE_OR_FALSE_VIEW"
    FREE_ANSWER_VIEW = "FREE_ANSWER_VIEW"


class Topic(CommonModel):
    class Meta:
        verbose_name = _("Топик")
        verbose_name_plural = _("Топики")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Название топика"),
    )


class Unit(CommonModel):
    class Meta:
        verbose_name = _("Юнит")
        verbose_name_plural = _("Юниты")

    topic = models.ForeignKey(
        to=Topic,
        on_delete=models.CASCADE,
        verbose_name=_("Топик"),
        related_name="units",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Название юнита"),
        default="Безымянный раздел"
    )

    objects = UnitManager()


class UnitTheoryElement(CommonModel):
    class Meta:
        verbose_name = _("Теоретический блок юнита")
        verbose_name_plural = _("Теоретическии блоки юнитов")

    unit = models.ForeignKey(
        to=Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Юнит"),
        related_name="theories",
    )
    type = models.CharField(
        max_length=60,
        choices=UnitTheoryElementType.choices,
        verbose_name=_("Тип элемента"),
    )
    content = models.JSONField(
        verbose_name=_("Контетнт элемента"),
        encoder=DjangoJSONEncoder,
    )


class UnitExerciseElement(CommonModel):
    class Meta:
        verbose_name = _("Упражнение юнита")
        verbose_name_plural = _("Упражнения юнитов")

    unit = models.ForeignKey(
        to=Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Юнит"),
        related_name="exercises",
    )
    type = models.CharField(
        max_length=60,
        choices=UnitExerciseElementType.choices,
        verbose_name=_("Тип элемента"),
    )
    content = models.JSONField(
        verbose_name=_("Контент элемента"), encoder=DjangoJSONEncoder
    )
