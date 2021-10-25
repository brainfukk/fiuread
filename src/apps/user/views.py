from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.authentication.models import FIUReadUser
from src.apps.authentication.serializers import FIUReadGetUserSerializer
from src.apps.utils.viewsets import ModelViewSetMixin

from .models import Event, UserPurchases, UserPurse, UserUnitRelation
from .serializers import (
    EventSerializer,
    UserPurchasesSerializer,
    UserPurseSerializer,
    UserUnitRelationSerializer,
)


class UserViewSet(ModelViewSetMixin):
    queryset = FIUReadUser.objects.all()
    serializer_class = FIUReadGetUserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserPurchasesViewSet(ModelViewSetMixin):
    queryset = UserPurchases.objects.all()
    serializer_class = UserPurchasesSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        instance = UserPurchases.objects.create(
            product_id=request.data.get("product_id"), user_id=request.user.id
        )
        user_purse = UserPurse.objects.get(user__id=request.user.id)
        user_purse.points = user_purse.points - instance.product.cost
        user_purse.save()

        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)


class UserPurseViewSet(ModelViewSetMixin):
    queryset = UserPurse.objects.all()
    serializer_class = UserPurseSerializer
    permission_classes = (IsAuthenticated,)


class EventViewSet(ModelViewSetMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


class UserUnitRelationViewSet(ModelViewSetMixin):
    queryset = UserUnitRelation.objects.all()
    serializer_class = UserUnitRelationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(user__id=self.request.user.id)
            .order_by("-progress")[:3]
        )
