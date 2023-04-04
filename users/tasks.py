from celery import shared_task
from .models import EmailCodes
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def mail_send(subject, message, from_email, to_emails):
    send_mail(subject,
              message,
              from_email,
              to_emails)
    return "Done"
