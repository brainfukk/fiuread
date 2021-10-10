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
    LIST_VIEW = "LIST_VIEW", "Список"

    PLAIN_TEXT_VIEW = "PLAIN_TEXT_VIEW", "Текст"

    IMAGE_VIEW = "IMAGE_VIEW", "Изображение"
    IMAGE_BETWEEN_TEXT = "IMAGE_BETWEEN_TEXT", "Изображение, между текстами"
    IMAGE_LEFT_TEXT_VIEW = "IMAGE_LEFT_TEXT_VIEW", "Изображение, текст слева"
    IMAGE_RIGHT_TEXT_VIEW = "IMAGE_RIGHT_TEXT_VIEW", "Изображение, текст справа"


class UnitExerciseElementType(models.TextChoices):
    FREE_ANSWER = "FREE_ANSWER", "СВОБОДНЫЙ ТИП ОТВЕТОВ"
    IN_TEXT = "IN_TEXT", "ВСТАВКА ОТВЕТОВ В ТЕКСТ"
    ANSWER_CHOICE = "ANSWER_CHOICE", "ВЫБРАТЬ ПРАВИЛЬНЫЙ ОТВЕТ"
    SCROLL_CHOICE = "SCROLL_CHOICE", "СКРОЛЛ ВВЕРХ-ВНИЗ"


class Topic(CommonModel):
    class Meta:
        verbose_name = _("Топик")
        verbose_name_plural = _("Топики")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Название топика"),
    )

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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
    content = models.CharField(
        max_length=600,
        verbose_name=_("Контетнт элемента"),
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
    content = models.CharField(
        max_length=500,
        verbose_name=_("Контент элемента"),
    )

    def __str__(self):
        return self.content


class UnitExerciseElementAnswer(CommonModel):
    class Meta:
        verbose_name = _("Варианты ответов для упражнения юнита")
        verbose_name_plural = _("Варианты ответов для упражнения юнитов")

    exercise = models.ForeignKey(
        to=UnitExerciseElement,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Упражнение юнита"),
        related_name="answers"
    )
    data = models.JSONField(
        verbose_name=_("Варинаты ответов или правильные ответы(зависит от типа упражнения)"),
        encoder=DjangoJSONEncoder,
        default=dict(
            variants=["data"],
            answers={0: 1}
        )
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Индикатор который указывает на правильность варинта(не для FREE_ANSWER_VIEW)")
    )

    def __str__(self):
        return "{} Ответы".format(str(self.exercise))
