from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """
    Асинхронная задача для отправки email-уведомления при успешном создании заказа.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return False

    subject = f'Order №{order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order.\n'
        f'Your order ID is {order.id}.'
    )

    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )
    return mail_sent