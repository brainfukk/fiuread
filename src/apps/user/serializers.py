from rest_framework import serializers

from src.apps.shop.serializers import ShopItemSerializer

from .models import Event, UserPurchases, UserPurse, UserUnitRelation


class UserPurchasesSerializer(serializers.ModelSerializer):
    product = ShopItemSerializer()

    class Meta:
        model = UserPurchases
        fields = ("user", "product", "is_active")


class UserPurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurse
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class UserUnitRelationSerializer(serializers.ModelSerializer):
    topic_name = serializers.SerializerMethodField()

    class Meta:
        model = UserUnitRelation
        fields = ("user", "unit", "progress", "topic_name")

    def get_topic_name(self, obj):
        return obj.unit.topic.name
