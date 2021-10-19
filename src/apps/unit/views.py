from rest_framework.permissions import IsAuthenticated, AllowAny

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
            user__id=self.request.user.id
        )

