import jwt
from datetime import datetime, timedelta
from django.conf import settings
from mail_templated import EmailMessage
from celery import shared_task
import time


def generate_password_reset_token(user):
    payload = {
        "user_id": user.id,
        "pwd_hash": user.password,  # capture current password hash
        "exp": datetime.utcnow() + timedelta(hours=48),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@shared_task
def send_email_reset_password(email, reset_url):
    time.sleep(10)
    email_obj = EmailMessage(
        "email/password_reset.tpl",  # template path
        {"reset_url": reset_url},
        settings.EMAIL_HOST_USER,
        to=[email],
    )
    email_obj.send()
