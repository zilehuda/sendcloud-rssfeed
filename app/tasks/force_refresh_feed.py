from app.celery import celery

from app.database import get_db
from app.services.feed_manager_service import force_update_feed
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery.task(name="force_refresh_feed")
def force_refresh_feed(feed_id):
    db = next(get_db())
    force_update_feed(db, feed_id)
