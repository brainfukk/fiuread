from rest_framework import serializers

from .models import FIUReadUser


class FIUReadGetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIUReadUser
        fields = ("id", "username", "email", "date_joined")


class FIUReadCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIUReadUser
        fields = ("username", "email", "password")


class FIUReadUserEmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIUReadUser
        fields = ("is_email_confirmed",)
