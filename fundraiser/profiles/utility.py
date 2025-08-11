import random
import uuid
from .tasks import send_email_task

def generate_random_otp():
  return str(random.randint(100000, 999999))

def create_token():
  return str(uuid.uuid4())

def send_queued_email(recipient_email, subject, html_content, template_name=None):
    send_email_task.delay(
        recipient_email=recipient_email,
        subject=subject,
        html_content=html_content,
        template_name=template_name
    )
    return True

def send_queued_email(recipient_email, subject, html_content, template_name=None):
    send_email_task.delay(
        recipient_email=recipient_email,
        subject=subject,
        html_content=html_content,
        template_name=template_name
    )
    return True