from typing import Optional

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.user.models import UserUnitRelation
from src.apps.utils.models import CommonModel


class UnitManager(models.Manager):
    def create_users_unit_relation(self, unit, users):
        data = [UserUnitRelation(user=user, unit=unit) for user in users]
        return UserUnitRelation.objects.bulk_create(data)

    def create_unit(self, topic, name, desc):
        unit = Unit.objects.create(topic=topic, name=name, description=desc)
        self.create_users_unit_relation(unit=unit, users=get_user_model().objects.all())
        return unit


class UnitTheoryElementType(models.TextChoices):
    LIST_VIEW = "LIST_VIEW", "Список"
    PLAIN_TEXT_VIEW = "PLAIN_TEXT_VIEW", "Текст"
    IMAGE_VIEW = "IMAGE_VIEW", "Изображение"
    HEADING = "HEADING", "Заголовок"


class UnitExerciseElementType(models.TextChoices):
    ANSWER_CHOICE = "ANSWER_CHOICE", "Выбрать правильный ответ"
    IN_TEXT_SELECT = "IN_TEXT_SELECT", "Выбор правильного ответа в тексте"
    FREE_IN_TEXT_ANSWER = "FREE_IN_TEXT_ANSWER", "Вписать правильный ответ в тексте"


class Topic(CommonModel):
    class Meta:
        verbose_name = _("Топик")
        verbose_name_plural = _("Топики")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Название топика"),
    )
    description = models.CharField(
        max_length=40, verbose_name=_("Описание раздела"), default="", blank=True
    )

    def get_progress(self, user_id: int) -> Optional[int]:
        progress = 0
        unit_user_relations_progress = self.units.filter(  # noqa
            related_users__user__id=user_id
        ).values_list("related_users__progress", flat=True)

        if not unit_user_relations_progress:
            return 0

        one_unit_weight = 100 // unit_user_relations_progress.count()
        for unit_user_relation_progress in unit_user_relations_progress:
            unit_weight = (one_unit_weight * unit_user_relation_progress) // 100
            progress += unit_weight
        return progress

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
        max_length=255, verbose_name=_("Название юнита"), default="Безымянный раздел"
    )
    description = models.CharField(
        max_length=100, verbose_name=_("Описание юнита"), default="Нет описания..."
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
        max_length=600, verbose_name=_("Контетнт элемента"), null=True, blank=True
    )
    image = models.ImageField(upload_to="unitassets", null=True, blank=True)
    order_number = models.IntegerField(default=0)


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
        max_length=500, verbose_name=_("Контент элемента"), null=True, blank=True
    )
    image = models.ImageField(upload_to="unitassets", null=True, blank=True)
    order_number = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class UnitExerciseElementAnswer(CommonModel):
    class Meta:
        verbose_name = _("Вариант ответа упражнения юнита")
        verbose_name_plural = _("Варианты ответов для упражнения юнитов")

    exercise = models.ForeignKey(
        to=UnitExerciseElement,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Упражнение юнита"),
        related_name="answers",
    )
    data = models.JSONField(
        verbose_name=_(
            "Варинаты ответов или правильные ответы(зависит от типа упражнения)"
        ),
        encoder=DjangoJSONEncoder,
        default=dict(variants=["data"], answers={0: 1}),
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_(
            "Индикатор который указывает на правильность варинта(не для FREE_ANSWER_VIEW)"
        ),
    )

    def __str__(self):
        return "{} Ответы".format(str(self.exercise))


class UnitUserAnswer(CommonModel):
    class Meta:
        verbose_name = _("Ответ юзера на вопрос")
        verbose_name_plural = _("Ответы юзеров на вопросы")

    user = models.ForeignKey(
        to="authentication.FIUReadUser",
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name=_("Пользователь"),
    )
    unit = models.ForeignKey(to=Unit, on_delete=models.CASCADE, verbose_name=_("Юнит"))
    exercise = models.ForeignKey(
        to=UnitExerciseElement,
        on_delete=models.CASCADE,
        related_name="user_answer",
        verbose_name=_("Упражнение"),
    )
    answer = models.ForeignKey(
        to=UnitExerciseElementAnswer,
        on_delete=models.CASCADE,
        verbose_name=_("Ответ пользователя"),
    )

    def __str__(self):
        return "<{}> {}".format(self.unit, self.exercise, self.answer)
