from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.utils.models import CommonModel


class EventItemType(models.TextChoices):
    UNIT_FINISHED = "UNIT_FINISHED"
    POINTS_EARNED = "POINTS_EARNED"
    PURCHASE = "PURCHASE"
    NOTIFICATION = "NOTIFICATION"


class UserPurse(CommonModel):
    class Meta:
        verbose_name = _("Кошелек пользователя")
        verbose_name_plural = _("Кошелький пользователей")

    user = models.ForeignKey(
        to="authentication.FIUReadUser",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="purse",
    )
    points = models.IntegerField(default=0, verbose_name=_("Счет пользователя"))

    def __str__(self):
        return "{} {}".format(self.user, str(self.points))


class UserPurchases(CommonModel):
    class Meta:
        verbose_name = _("Преобретение пользователя")
        verbose_name_plural = _("Преобретения пользователя")

    user = models.ForeignKey(
        to="authentication.FIUReadUser",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="purchases",
    )
    product = models.ForeignKey(
        to="shop.ShopItem",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Продукт"),
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.product.name)  # noqa


class Event(CommonModel):
    class Meta:
        verbose_name = _("Ивент пользователя")
        verbose_name_plural = _("Ивенты пользователей")

    user = models.ForeignKey(
        to="authentication.FIUReadUser",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="events",
    )
    type = models.CharField(
        max_length=30, choices=EventItemType.choices, verbose_name=_("Тип ивента")
    )
    message = models.CharField(
        max_length=255,
        verbose_name=_("Текст ивента"),
    )
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class UserUnitRelation(CommonModel):
    class Meta:
        verbose_name = _("Отношение юнита и пользователя")
        verbose_name_plural = _("Отношений юнитов и пользователей")

    user = models.ForeignKey(
        to="authentication.FIUReadUser",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="related_units",
    )
    unit = models.ForeignKey(
        to="unit.Unit",
        on_delete=models.CASCADE,
        verbose_name=_("Юнит"),
        related_name="related_users",
    )
    progress = models.IntegerField(
        default=0, verbose_name=_("Прогресс прохождения юнита")
    )
