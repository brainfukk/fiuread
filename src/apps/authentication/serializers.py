from rest_framework import serializers

from .models import FIUReadUser
from src.apps.shop.serializers import ShopItemSerializer


class FIUReadGetUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = FIUReadUser
        fields = ("id", "username", "email", "date_joined", "avatar", "points")

    def get_points(self, obj):
        return obj.purse.last().points

    def get_avatar(self, obj):
        purchases = obj.purchases.filter(is_active=True).last()
        if purchases is None:
            return purchases
        return ShopItemSerializer(purchases.product, many=False).data


class FIUReadCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIUReadUser
        fields = ("username", "email", "password")


class FIUReadUserEmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIUReadUser
        fields = ("is_email_confirmed",)
