import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

django.setup()  # initialize Django

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: [
    "songs",
    "playlists", 
    "users",
])