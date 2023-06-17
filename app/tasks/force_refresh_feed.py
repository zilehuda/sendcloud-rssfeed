from celery.utils.log import get_task_logger

from app.celery_app import app
from app.database import get_db
from app.services.feed_manager_service import force_update_feed

logger = get_task_logger(__name__)


@app.task(name="force_refresh_feed")
def force_refresh_feed(feed_id: int) -> None:
    logger.info(f"Forcing refresh of feed {feed_id}")
    db = next(get_db())
    force_update_feed(db, feed_id)
    logger.info(f"Feed {feed_id} successfully refreshed")
