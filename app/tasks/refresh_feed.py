from celery.utils.log import get_task_logger

from app.celery import celery
from app.database import get_db
from app.models import Feed
from app.services.rss_feed_services import RSSFeedUpdater

logger = get_task_logger(__name__)


@celery.task(bind=True, name="refresh_feed")
def refresh_feed(self, feed_id: int):
    try:
        db = next(get_db())
        feed = db.query(Feed).filter_by(id=feed_id).first()
        if feed:
            rss_feed_service = RSSFeedUpdater(db, feed.id)
            rss_feed_service.fetch_and_update_feed()
    except Exception as exc:
        # Retry the task with a back-off mechanism
        delays = [120, 300, 480]  # Delays in seconds (2, 5, and 8 minutes)
        retry_count = self.request.retries
        if retry_count < len(delays):
            delay = delays[self.request.retries]
            self.retry(exc=exc, countdown=delay)
