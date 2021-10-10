from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.authentication.models import FIUReadUser
from src.apps.authentication.serializers import FIUReadGetUserSerializer
from src.apps.utils.viewsets import ModelViewSetMixin


class UserViewSet(ModelViewSetMixin):
    queryset = FIUReadUser.objects.all()
    serializer_class = FIUReadGetUserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
