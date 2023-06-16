from celery import Celery
from celery.schedules import crontab


print("NAME: ", __name__)
celery = Celery(__name__)
celery.conf.broker_url = "amqp://guest:guest@localhost:5672/"
celery.conf.result_backend = "rpc://"

celery.autodiscover_tasks(["app.tasks"])

celery.conf.beat_schedule = {
    "refresh_feed_every_5_minutes": {
        "task": "refresh_feeds",
        "schedule": crontab(minute="*/5"),
    },
}
