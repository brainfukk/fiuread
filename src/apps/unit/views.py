from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from src.apps.utils.viewsets import ModelViewSetMixin

from .models import (
    Topic,
    Unit,
    UnitExerciseElement,
    UnitExerciseElementAnswer,
    UnitTheoryElement,
    UnitUserAnswer,
)
from src.apps.user.models import Event, UserPurse
from .seriazliers import (
    TopicSerializer,
    UnitExerciseElementAnswerSerializer,
    UnitExerciseElementSerializer,
    UnitSerializer,
    UnitTheoryElementSerializer,
    UnitUserAnswerSerializer,
)
from .utils import AnswersMixin


class TopicViewSet(ModelViewSetMixin):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (AllowAny,)


class UnitViewSet(ModelViewSetMixin):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(topic__id=self.request.query_params.get("topic_id"))
        )


class UnitSearchViewSet(ModelViewSetMixin):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def list(self, request, *args, **kwargs):
        items = []
        units = self.get_queryset()
        search_phrase = request.query_params.get("search_phrase", "").lower()

        if not search_phrase.strip():
            return Response([])

        for unit in units:
            if search_phrase in unit.name.lower():
                items.append(unit)
                continue

            if search_phrase in unit.description.lower():
                items.append(unit)
                continue

            theory_elements = unit.theories.all()
            for theory_element in theory_elements:
                if search_phrase in theory_element.content.lower():
                    items.append(unit)
                    break

        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class UnitTheoryElementViewSet(ModelViewSetMixin):
    queryset = UnitTheoryElement.objects.all().select_related("unit")
    serializer_class = UnitTheoryElementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(unit__id=self.request.query_params.get("unit_id"))
            .order_by("order_number")
        )


class UnitExercisesElementViewSet(ModelViewSetMixin):
    queryset = UnitExerciseElement.objects.all()
    serializer_class = UnitExerciseElementSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(unit__id=self.request.query_params.get("unit_id"))
            .order_by("order_number")
        )


class UnitExercisesAnswersViewSet(ModelViewSetMixin):
    queryset = UnitExerciseElementAnswer
    serializer_class = UnitExerciseElementAnswerSerializer
    permission_classes = (IsAuthenticated,)


class UnitUserAnswerViewSet(ModelViewSetMixin):
    queryset = UnitUserAnswer.objects.all()
    serializer_class = UnitUserAnswerSerializer
    permission_classes = (IsAuthenticated,)
    event_message = "Поздравляем! Вы закончили юнит {}"
    event_coins_earned_message = "На ваш счет зачислено {} баллов"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                user__id=self.request.user.id,
                unit__id=self.request.query_params.get("unit_id"),
            )
        )

    def get_answer_var(self, exercise_id: int):
        exercise = UnitExerciseElementAnswer.objects.filter(exercise__id=exercise_id)
        if len(exercise) == 1 and exercise[0].type == "IN_TEXT_SELECT":
            return exercise[0]
        return

    def get_exercise(self, exercise_id: int):
        return UnitExerciseElement.objects.get(id=exercise_id)

    def create(self, request, *args, **kwargs):
        unit_id = request.data.get("unit_id")
        answers = request.data.get("answers")

        items = []
        points = 0
        unit_obj = Unit.objects.get(id=unit_id)

        for key, value in answers.items():
            exercise = self.get_exercise(key)
            try:
                unit = UnitUserAnswer.objects.get(
                    user__id=request.user.id,
                    unit__id=unit_id,
                    exercise_id=int(key),
                )
            except UnitUserAnswer.DoesNotExist:  # noqa
                unit = UnitUserAnswer.objects.create(
                    user_id=request.user.id,
                    unit_id=unit_id,
                    exercise_id=int(key),
                )
                points += 1

            if exercise.type in ["IN_TEXT_SELECT", "FREE_IN_TEXT_ANSWER"]:
                db_answer = exercise.answers.last().data
                db_answer["user"] = value
                unit.json_answer = db_answer
            else:
                db_answer = exercise.answers.filter(id=value).last()
                unit.answer = db_answer

            unit.save()
            items.append(unit)

        answers_mixin = AnswersMixin(items=items)
        correct, questions = answers_mixin.check()

        all_answers = unit_obj.exercises.count()
        user_answers = len(items)

        progress = (user_answers * 100) // all_answers

        user_to_unit_relation = unit_obj.related_users.filter(
            user__id=request.user.id
        ).last()
        user_to_unit_relation.progress = progress
        user_to_unit_relation.save()

        Event.objects.create(
            user=request.user,
            type='NOTIFICATION',
            message=self.event_message.format(unit_obj.name)
        )

        user_purse = UserPurse.objects.get(user__id=request.user.id)
        user_purse.points += points
        user_purse.save()
        Event.objects.create(
            user=request.user,
            type='NOTIFICATION',
            message=self.event_coins_earned_message.format(str(points))
        )
        return Response({"correct": "{}/{}".format(correct, questions)})
