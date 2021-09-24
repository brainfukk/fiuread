from django.conf import settings
from django.core.mail import send_mail

from src.configs.celery import app


@app.task
def send_email(username: str, email: str, confirmation_code: str):
    send_mail(
        subject="Hey {}! There is your confirmation code:".format(username),
        message="Введите этот код: {}".format(confirmation_code),
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=False,
        recipient_list=[email],
    )
