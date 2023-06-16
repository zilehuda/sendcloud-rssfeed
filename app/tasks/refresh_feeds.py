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

from app.tasks.refresh_feed import refresh_feed

logger = get_task_logger(__name__)


@celery.task(name="refresh_feeds")
def refresh_feeds():
    db = next(get_db())
    feeds = db.query(Feed).all()
    for feed in feeds:
        print("haha")
        refresh_feed.delay(feed.id)
