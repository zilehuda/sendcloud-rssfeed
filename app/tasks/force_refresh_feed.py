from app.celery import celery
import time

from app.database import get_db
from app.models import Feed
from app.services.feed_manager_service import fetch_feed, force_update_feed
from app.services.rss_feed_services import (
    RSSFeedFetcher,
    RSSFeedUpdater,
    RSSFeedCreator,
)
from typing import Optional
from celery.utils.log import get_task_logger

from app.services.user_service import assign_feed_to_user
from datetime import timedelta

logger = get_task_logger(__name__)


@celery.task(name="force_refresh_feed")
def force_refresh_feed(feed_id):
    db = next(get_db())
    force_update_feed(db, feed_id)
