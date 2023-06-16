from datetime import datetime, timezone
from time import mktime
from typing import Optional

from feedparser import FeedParserDict
from sqlalchemy.orm import Session

from app.models import Feed, Post

from .feed_fetcher import RSSFeedFetcher


class RSSFeedCreator:
    def __init__(self, feed_url: str, fetcher: RSSFeedFetcher, db: Session) -> None:
        self.feed_url = feed_url
        self._db = db
        self._fetcher = fetcher

    def _save_feed(self, feed: FeedParserDict) -> Feed:
        try:
            _feed = feed.feed
            latest_post_id: Optional[str] = None
            if len(feed.entries):
                latest_post_id = feed.entries[0].id

            logo: str = ""
            if "image" in _feed:
                logo = _feed.image.href
            elif "logo" in _feed:
                logo = _feed.logo

            feed_obj: Feed = Feed(  # type: ignore[misc]
                title=_feed.title,
                website=_feed.link,
                feed_url=self.feed_url,
                logo=logo,
                latest_post_id=latest_post_id,
            )

            self._db.add(feed_obj)
            for entry in feed.entries:
                post_obj = Post(
                    post_id=entry.id,
                    title=entry.title,
                    summary=entry.summary,
                    author=entry.author,
                    post_url=entry.link,
                    published_at=datetime.fromtimestamp(
                        mktime(entry.published_parsed),
                        timezone.utc,
                    ),
                    feed=feed_obj,
                )
                self._db.add(post_obj)
            self._db.commit()
            self._db.refresh(feed_obj)
            return feed_obj
        except Exception as e:
            raise e

    def fetch_and_save_feed(self) -> Optional[Feed]:
        try:
            existing_feed = (
                self._db.query(Feed).filter_by(feed_url=self.feed_url).first()
            )
            if existing_feed:
                return existing_feed
            else:
                feed = self._fetcher.fetch_feed()
                if feed:
                    return self._save_feed(feed)
                else:
                    print("Error occurred while fetching the feed.")
                    return None
        except Exception as e:
            raise e
