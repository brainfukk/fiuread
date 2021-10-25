from django.contrib import admin

from .models import ShopItem


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    search_fields = ("name", "cost")
    list_display = ("name", "cost", "source")
