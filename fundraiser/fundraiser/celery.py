"""Celery configuration for the psvq project.
This module sets up the Celery application for the project, allowing it to
process asynchronous tasks using the Django settings.
This file is typically located in the psvq/psvq directory.
It is important to ensure that the Celery app is correctly configured
to work with Django's settings and that it can discover tasks
from all registered Django apps.
"""
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundraiser.settings')

# Create the Celery app
app = Celery('fundraiser')

# Use a string here instead of a direct import
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()