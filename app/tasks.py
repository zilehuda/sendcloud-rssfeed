from app.celery import celery
import time

from app.database import get_db
from app.models import Feed
from app.services.feed_manager_service import fetch_feed
from app.services.rss_feed_services import (
    RSSFeedFetcher,
    RSSFeedUpdater,
    RSSFeedCreator,
)
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


@celery.task(name="refresh_feed")
def refresh_feed(feed_id):
    db = next(get_db())
    feed = db.query(Feed).filter_by(id=feed_id).first()
    if feed:
        feed_fetcher = RSSFeedFetcher(feed.feed_url)
        rss_feed_service = RSSFeedUpdater(feed.id, feed_fetcher, db)
        rss_feed_service.fetch_and_update_feed()


@celery.task(name="refresh_feeds")
def refresh_feeds():
    logger.info("HAHAHAHAHH")
    time.sleep(2)
    db = next(get_db())
    feeds = db.query(Feed).all()
    for feed in feeds:
        print("haha")
        refresh_feed.delay(feed.id)
