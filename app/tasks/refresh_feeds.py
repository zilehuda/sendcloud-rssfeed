from app.celery import celery

from app.database import get_db
from app.models import Feed
from celery.utils.log import get_task_logger


from app.tasks.refresh_feed import refresh_feed

logger = get_task_logger(__name__)


@celery.task(name="refresh_feeds")
def refresh_feeds():
    db = next(get_db())
    feeds = db.query(Feed).all()
    for feed in feeds:
        print("haha")
        refresh_feed.delay(feed.id)