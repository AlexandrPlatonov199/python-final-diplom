from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from orders.celery import app
from .models import ConfirmEmailToken


@app.task
def email_confirmation_token(user_id):
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    msg = EmailMultiAlternatives(
        f"Токен для подверждения электронной почты {token.user.email}",
        token.key,
        settings.EMAIL_HOST_USER,
        [token.user.email]
    )
    msg.send()


@app.task
def email_reset_password_token(user, key, email):
    msg = EmailMultiAlternatives(
        f"Токен для сброса пароля для {user}",
        key,
        settings.EMAIL_HOST_USER,
        [email]
    )
    msg.send()