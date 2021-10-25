from rest_framework.permissions import AllowAny

from src.apps.utils.viewsets import ModelViewSetMixin

from .models import ShopItem
from .serializers import ShopItemSerializer


class ShopItemsViewSet(ModelViewSetMixin):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer
    permission_classes = (AllowAny,)
