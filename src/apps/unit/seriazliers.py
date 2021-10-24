from rest_framework import serializers

from src.apps.authentication.serializers import FIUReadGetUserSerializer
from .models import (
    Topic,
    Unit,
    UnitTheoryElement,
    UnitExerciseElement,
    UnitUserAnswer,
    UnitExerciseElementAnswer
)
from .utils import AnswersMixin


class TopicSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ("id", "name", "progress", "description")

    def get_name(self, obj):
        return obj.name[:30]

    def get_progress(self, obj):
        request = self.context["request"]
        return obj.get_progress(user_id=request.user.id)


class UnitSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    progress = serializers.SerializerMethodField()
    short_content = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ("id", "topic", "name", "progress", "short_content")

    def get_short_content(self, obj):
        return obj.description

    def get_progress(self, obj):
        request = self.context["request"]
        user_to_unit_relation = obj.related_users.filter(
            user__id=request.user.id
        ).last()
        if user_to_unit_relation is None:
            return None
        return user_to_unit_relation.progress


class UnitTheoryElementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model = UnitTheoryElement
        fields = ("id", "unit", "type", "content", "image")


class UnitExerciseElementAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitExerciseElementAnswer
        fields = ("id", "data", "is_correct")


class UnitExerciseElementSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UnitExerciseElement
        fields = ("id", "unit", "type", "image", "content", "answers")

    def get_answers(self, obj):
        return UnitExerciseElementAnswerSerializer(
            obj.answers.all(), many=True
        ).data


class UnitUserAnswerSerializer(serializers.ModelSerializer):
    answer = UnitExerciseElementAnswerSerializer()
    exercise_type = serializers.SerializerMethodField()

    class Meta:
        model = UnitUserAnswer
        fields = ("id", "exercise", "exercise_type", "answer")

    def get_exercise_type(self, obj):
        return obj.exercise.type
