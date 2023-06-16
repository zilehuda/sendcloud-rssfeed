from app.celery import celery

from app.database import get_db
from app.models import Feed
from app.services.feed_manager_service import fetch_feed
from typing import Optional
from celery.utils.log import get_task_logger

from app.services.user_service import assign_feed_to_user

logger = get_task_logger(__name__)


@celery.task(name="fetch_and_assign_feed_to_user")
def fetch_and_assign_feed_to_user(user_id, feed_url):
    db = next(get_db())
    feed: Optional[Feed] = fetch_feed(db, feed_url)
    if feed:
        assign_feed_to_user(db, user_id, feed)