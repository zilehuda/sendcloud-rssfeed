from celery.utils.log import get_task_logger

from app.celery_app import app
from app.constants import FetchStatus
from app.database import get_db
from app.models import Feed
from .refresh_feed import refresh_feed

logger = get_task_logger(__name__)


@app.task(name="refresh_feeds")
def refresh_feeds():
    db = next(get_db())
    feeds = db.query(Feed).filter_by(fetch_status=FetchStatus.COMPLETED.value).all()
    logger.info(f"Refreshing {len(feeds)} feeds")
    for feed in feeds:
        refresh_feed.delay(feed.id)
