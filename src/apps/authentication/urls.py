from django.urls import path
from rest_framework_simplejwt import views

from .views import (
    EmailConfirmationView,
    RegistrationPipelineViewSet,
    RegistrationViewSet,
)

urlpatterns = [
    path("login/", views.token_obtain_pair, name="token_obtain_pair"),
    path("refresh/", views.token_refresh, name="token_refresh"),
    path(
        "register/step-1/",
        RegistrationViewSet.as_view({"post": "step_1"}),
        name="register-1",
    ),
    path(
        "register/step-2/",
        EmailConfirmationView.as_view({"post": "confirm_post"}),
        name="register-2",
    ),
    path("register/pipeline/", RegistrationPipelineViewSet.as_view({"get": "handle"})),
]
