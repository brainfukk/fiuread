from rest_framework import serializers

from .models import ShopItem


class ShopItemSerializer(serializers.ModelSerializer):
    buy_method = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = ("id", "name", "cost", "source", "buy_method")

    def get_buy_method(self, obj):
        return {"is_coin_available": True, "is_level_available": True}
