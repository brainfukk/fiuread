from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.apps.utils.redis_tools import (
    check_user_confirmation_status,
    check_user_token,
    confirm_user_token,
    construct_email_token_register_key,
    set_email_token_confirmation,
)
from src.apps.utils.viewsets import ModelViewSetMixin

from .models import FIUReadUser
from .serializers import (
    FIUReadCreateUserSerializer,
    FIUReadGetUserSerializer,
    FIUReadUserEmailConfirmationSerializer,
)
from .tasks import send_email


class RegistrationPipelineViewSet(ModelViewSetMixin):
    queryset = FIUReadUser.objects.all()
    serializer_class = FIUReadGetUserSerializer
    permission_classes = (AllowAny,)

    def handle(self, request, *args, **kwargs):
        type_ = request.query_params.get("type")
        if type_ == "username":
            return self.check_username(request, *args, **kwargs)

    def check_username(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        if username is None:
            raise APIException(
                "username is not provided", code="400;%s" % "USERNAME_IS_NOT_PROVIDED"
            )

        try:
            user = self.get_queryset().get(username=username)
        except FIUReadUser.DoesNotExist:  # noqa
            user = None

        serializer = self.get_serializer(user, many=False)

        if user is None:
            return Response({"detail": False})
        return Response(serializer.data)


class RegistrationViewSet(ModelViewSetMixin):
    celery_task = send_email
    queryset = FIUReadUser.objects.all()
    serializer_class = FIUReadCreateUserSerializer

    def step_1(self, request, *args, **kwargs):
        username = request.data.get("username")
        user_email = request.data.get("email")

        confirmation_code = construct_email_token_register_key(
            username=username, user_email=user_email
        )
        set_email_token_confirmation(
            key=confirmation_code, username=username, user_email=user_email
        )
        self.celery_task.delay(
            username=username, confirmation_code=confirmation_code, email=user_email
        )
        return Response(
            {"msg": "message with confirmation code has been sent to your email"}
        )

    def step_2(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        is_confirmed = check_user_confirmation_status(username=username, email=email)
        if not is_confirmed:
            raise APIException(
                "User didn't approved confirmation code.",
                code="400;%s" % "NOT_APPROVED_CONFIRM_CODE",
            )

        user = FIUReadUser.objects.create_user(
            username=username, email=email, password=password, is_email_confirmed=True
        )
        user.save()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=200)


class EmailConfirmationView(ModelViewSetMixin):
    queryset = FIUReadUser.objects.all()
    serializer_class = FIUReadUserEmailConfirmationSerializer

    def verify(self, data, confirmation_code):
        username = data.get("username")
        email = data.get("email")
        is_correct = check_user_token(
            username=username, user_email=email, key=confirmation_code
        )
        if not is_correct:
            raise APIException(
                "Confirmation code is not correct",
                code="400;%s" % "CONFIRMATION_CODE_VALIDATION_ERROR",
            )

        confirm_user_token(key=confirmation_code)
        return Response({"msg": True}, status=200)

    def confirm_post(self, request, *args, **kwargs):
        confirmation_code = request.data.get("token")
        return self.verify(data=request.data, confirmation_code=confirmation_code)
