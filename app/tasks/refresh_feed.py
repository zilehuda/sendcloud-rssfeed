from app.celery_app import app
from app.constants import FetchStatus
from app.database import get_db
from app.models import Feed
from app.services import feed_service
from app.services.rss_feed_services import RSSFeedUpdater
from app.services import feed_manager_service


@app.task(bind=True, name="refresh_feed")
def refresh_feed(self, feed_id: int):
    # TODO: split stuff into services and repositories.
    try:
        db = next(get_db())
        feed_manager_service.refresh_feed(db, feed_id)
    except Exception as exc:
        # Retry the task with a back-off mechanism
        delays = [120, 300, 480]  # Delays in seconds (2, 5, and 8 minutes)
        retry_count = self.request.retries
        if retry_count == 0:
            feed_service.change_feed_fetch_status(
                next(get_db()), feed_id, FetchStatus.RETRYING
            )
        if retry_count < len(delays):
            delay = delays[self.request.retries]
            self.retry(exc=exc, countdown=delay)
        else:
            feed_service.change_feed_fetch_status(
                next(get_db()), feed_id, FetchStatus.FAILED
            )
