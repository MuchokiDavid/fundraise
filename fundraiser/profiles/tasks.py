"""
This module contains Celery tasks for sending emails.
This task is designed to send emails asynchronously using Celery.
It uses Django's email backend to send HTML emails and includes error handling
for retries in case of failure.
It is typically used in scenarios where email notifications are required,
such as user registration, password resets, or other notifications.
It is important to ensure that the Celery worker is running
to process these tasks.
"""
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Shared task to send email
@shared_task(bind=True, max_retries=3, default_retry_delay=300, rate_limit='10/m')
def send_email_task(self, recipient_email, subject, html_content, template_name=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, '', from_email, [recipient_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient_email}: {str(exc)}")
        raise self.retry(exc=exc)