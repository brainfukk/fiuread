from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import FIUReadUserManager


class UserPlan(models.TextChoices):
    FREE = "FREE_PLAN", "Бесплатная подписка"
    PREMIUM = "PREMIUM_PLAN", "Премиальная подписка"


class FIUReadUser(AbstractUser):
    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    is_email_confirmed = models.BooleanField(
        verbose_name=_("Подтвердил ли пользователь свой email"), default=False
    )
    plan = models.CharField(
        choices=UserPlan.choices,
        default=UserPlan.FREE,
        max_length=30,
        verbose_name=_("Подписка пользователя")
    )

    objects = FIUReadUserManager()

    def __str__(self):
        return self.username
