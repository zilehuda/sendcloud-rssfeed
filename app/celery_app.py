import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv(".env")
app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


app.autodiscover_tasks(["app.tasks"])

app.conf.beat_schedule = {
    "refresh_feed_every_5_minutes": {
        "task": "refresh_feeds",
        "schedule": crontab(minute="*/5"),
    },
}
