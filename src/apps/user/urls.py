from django.urls import path

from .views import UserViewSet


urlpatterns = [
    path("info/", UserViewSet.as_view({"get": "retrieve"}), name="user-info")
]
