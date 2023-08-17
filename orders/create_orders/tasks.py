from orders.celery import app
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from users_auth.models import User


@app.task
def new_order_confirm_email(user_id, order_id, **kwargs):
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        f'Статус заказа id{order_id} обновлен',
        f'Заказ id{order_id} сформирован',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()