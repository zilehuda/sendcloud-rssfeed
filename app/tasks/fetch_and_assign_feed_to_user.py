from typing import Optional

from celery.utils.log import get_task_logger
from app.celery_app import app
from app.database import get_db
from app.models import Feed
from app.services.feed_manager_service import fetch_feed
from app.services.user_service import assign_feed_to_user

logger = get_task_logger(__name__)


@app.task(name="fetch_and_assign_feed_to_user")
def fetch_and_assign_feed_to_user(user_id, feed_url):
    logger.info(f"Fetching and assigning feed '{feed_url}' to user {user_id}")

    db = next(get_db())
    feed: Optional[Feed] = fetch_feed(db, feed_url)
    if feed:
        assign_feed_to_user(db, user_id, feed)
        logger.info(
            f"Feed '{feed_url}' successfully fetched and assigned to user {user_id}"
        )
