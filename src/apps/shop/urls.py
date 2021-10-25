from django.urls import path

from .views import ShopItemsViewSet

urlpatterns = [path("items/", ShopItemsViewSet.as_view({"get": "list"}))]
