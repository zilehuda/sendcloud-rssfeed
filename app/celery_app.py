from celery import Celery
from celery.schedules import crontab

app = Celery(__name__)
app.conf.broker_url = "amqp://guest:guest@localhost:5672/"
app.conf.result_backend = "rpc://"

app.autodiscover_tasks(["app.tasks"])

app.conf.beat_schedule = {
    "refresh_feed_every_5_minutes": {
        "task": "refresh_feeds",
        "schedule": crontab(minute="*/5"),
    },
}
