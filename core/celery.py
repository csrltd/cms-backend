import os
from celery import Celery
from django.conf import settings

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create Celery application instance
app = Celery("core")

# Load Celery settings from Django settings.py
# All CELERY_* variables will be read
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    This is a simple debug task to confirm Celery is working.
    Run it with:
        celery -A core worker -l info
    Then call:
        debug_task.delay()
    """
    print(f"Request: {self.request!r}")
