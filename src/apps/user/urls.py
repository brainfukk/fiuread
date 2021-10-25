from django.urls import path

from .views import (
    EventViewSet,
    UserPurchasesViewSet,
    UserPurseViewSet,
    UserUnitRelationViewSet,
    UserViewSet,
)

urlpatterns = [
    path("info/", UserViewSet.as_view({"get": "retrieve"}), name="user-info"),
    path("purchases/", UserPurchasesViewSet.as_view({"get": "list", "post": "create"})),
    path("purse/", UserPurseViewSet.as_view({"get": "list"})),
    path("events/", EventViewSet.as_view({"get": "list"})),
    path("user_unit_relates/", UserUnitRelationViewSet.as_view({"get": "list"})),
]
