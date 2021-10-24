from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from src.apps.utils.viewsets import ModelViewSetMixin
from .models import (
    Topic,
    Unit,
    UnitTheoryElement,
    UnitExerciseElement,
    UnitUserAnswer,
    UnitExerciseElementAnswer
)
from .seriazliers import (
    TopicSerializer,
    UnitSerializer,
    UnitTheoryElementSerializer,
    UnitExerciseElementSerializer,
    UnitExerciseElementAnswerSerializer,
    UnitUserAnswerSerializer
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
        return super().get_queryset().filter(
            topic__id=self.request.query_params.get("topic_id")
        )


class UnitTheoryElementViewSet(ModelViewSetMixin):
    queryset = UnitTheoryElement.objects.all().select_related("unit")
    serializer_class = UnitTheoryElementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(
            unit__id=self.request.query_params.get("unit_id")
        ).order_by('order_number')


class UnitExercisesElementViewSet(ModelViewSetMixin):
    queryset = UnitExerciseElement.objects.all()
    serializer_class = UnitExerciseElementSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return super().get_queryset().filter(
            unit__id=self.request.query_params.get("unit_id")
        ).order_by("order_number")


class UnitExercisesAnswersViewSet(ModelViewSetMixin):
    queryset = UnitExerciseElementAnswer
    serializer_class = UnitExerciseElementAnswerSerializer
    permission_classes = (IsAuthenticated,)


class UnitUserAnswerViewSet(ModelViewSetMixin):
    queryset = UnitUserAnswer.objects.all()
    serializer_class = UnitUserAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(
            user__id=self.request.user.id,
            unit__id=self.request.query_params.get("unit_id")
        )

    def get_answer_var(self, exercise_id: int):
        exercise = UnitExerciseElementAnswer.objects.filter(exercise__id=exercise_id)
        if len(exercise) == 1 and exercise[0].type == 'IN_TEXT_SELECT':
            return exercise[0]
        return

    def get_exercise(self, exercise_id: int):
        return UnitExerciseElement.objects.get(id=exercise_id)

    def create(self, request, *args, **kwargs):
        unit_id = request.data.get('unit_id')
        answers = request.data.get('answers')

        items = []
        unit_obj = Unit.objects.get(id=unit_id)

        for key, value in answers.items():
            exercise = self.get_exercise(key)

            if exercise.type == "IN_TEXT_SELECT":
                db_answer = exercise.answers.last()
                db_answer.data['user'] = value
                db_answer.save()
            else:
                db_answer = exercise.answers.filter(id=value).last()

            try:
                unit = UnitUserAnswer.objects.get(
                    user__id=request.user.id,
                    unit__id=unit_id,
                    exercise_id=int(key),
                )
                unit.answer = db_answer
                unit.save()
            except UnitUserAnswer.DoesNotExist:  # noqa
                unit = UnitUserAnswer.objects.create(
                    user_id=request.user.id,
                    unit_id=unit_id,
                    exercise_id=int(key),
                    answer=db_answer
                )
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

        return Response({"correct": "{}/{}".format(correct, questions)})
