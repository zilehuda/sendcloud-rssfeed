import logging

from celery.utils.log import get_task_logger

from app.celery_app import app
from app.constants import FetchStatus
from app.database import get_db
from app.models import Feed
from app.services import feed_service
from app.services.rss_feed_services import RSSFeedUpdater
from app.services import feed_manager_service

logger = get_task_logger(__name__)


@app.task(bind=True, name="refresh_feed")
def refresh_feed(self, feed_id: int):
    logger.info(f"Refreshing feed {feed_id}")
    try:
        db = next(get_db())
        feed_manager_service.refresh_feed(db, feed_id)
    except Exception as exc:
        logger.error(f"Error refreshing feed {feed_id}: {exc}")

        # Retry the task with a back-off mechanism
        delays = [120, 300, 480]  # Delays in seconds (2, 5, and 8 minutes)
        retry_count = self.request.retries
        if retry_count == 0:
            logger.info(
                f"Changing fetch status of feed {feed_id} to {FetchStatus.RETRYING}"
            )
            feed_service.change_feed_fetch_status(
                next(get_db()), feed_id, FetchStatus.RETRYING
            )
        if retry_count < len(delays):
            delay = delays[self.request.retries]
            logger.info(f"Retrying task for feed {feed_id} after {delay} seconds")
            self.retry(exc=exc, countdown=delay)
        else:
            logger.info(
                f"Changing fetch status of feed {feed_id} to {FetchStatus.FAILED}"
            )
            feed_service.change_feed_fetch_status(
                next(get_db()), feed_id, FetchStatus.FAILED
            )
        logger.info(f"Feed refresh task for {feed_id} completed")
