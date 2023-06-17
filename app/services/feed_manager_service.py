from typing import Optional

from sqlalchemy.orm import Session

from app.models import Feed
from app.repositories.feed_repository import FeedRepository
from app.services.rss_feed_services import RSSFeedCreator, RSSFeedUpdater


def fetch_feed(db: Session, feed_url: str) -> Optional[Feed]:
    rss_feed_service = RSSFeedCreator(db, feed_url)
    feed = rss_feed_service.fetch_and_save_feed()
    return feed


def force_update_feed(
    db: Session,
    feed_id: int,
) -> None:
    rss_feed_service = RSSFeedUpdater(db, feed_id)
    rss_feed_service.fetch_and_update_feed()


def refresh_feed(db: Session, feed_id: int) -> None:
    feed_repository = FeedRepository(db)
    feed: Feed = feed_repository.get_feed_by_id(feed_id)
    if feed:
        rss_feed_service = RSSFeedUpdater(db, feed.id)
        rss_feed_service.fetch_and_update_feed()
