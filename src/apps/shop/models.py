from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.utils.models import CommonModel


class ShopItem(CommonModel):
    class Meta:
        verbose_name = _("Продукт магазина")
        verbose_name_plural = _("Продукты магазина")

    name = models.CharField(
        max_length=50,
        verbose_name=_("Название предмета"),
    )
    cost = models.IntegerField(default=0)
    source = models.ImageField(upload_to="unitassets", null=True, blank=True)

    def __str__(self):
        return self.name
