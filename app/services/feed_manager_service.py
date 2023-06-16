from sqlalchemy.orm import Session
from typing import Optional
from app.models import Feed
from app.repositories.feed_repository import FeedRepository
from app.services.rss_feed_services import (
    RSSFeedFetcher,
    RSSFeedCreator,
    RSSFeedUpdater,
)


def fetch_feed(db: Session, feed_url: str) -> Optional[Feed]:
    feed_fetcher = RSSFeedFetcher(feed_url)
    rss_feed_service = RSSFeedCreator(feed_url, feed_fetcher, db)
    feed = rss_feed_service.fetch_and_save_feed()
    return feed


def update_feed(
    db: Session,
    feed_id: str,
) -> Optional[Feed]:
    rss_feed_service = RSSFeedUpdater(db, feed_id)
    rss_feed_service.fetch_and_update_feed()
