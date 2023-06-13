from datetime import datetime, timezone
from time import mktime

import feedparser
from feedparser import FeedParserDict
from sqlalchemy.orm import Session

from app.models import Feed, Post
from app.services.feed_service import FeedService


class RSSFeedService(FeedService):
    def __init__(self, feed_url, db: Session) -> None:
        self.feed_url = feed_url
        self._db = db

    def fetch_feed(self) -> FeedParserDict:
        try:
            feed = feedparser.parse(self.feed_url)
            return feed
        except Exception as e:
            # Handle the exception according to your requirements
            print(f"Error fetching feed: {str(e)}")
            return None

    def _save_feed(self, feed):
        try:
            _feed = feed.feed
            feed_obj = Feed(
                title=_feed.title,
                website=_feed.link,
                feed_url=self.feed_url,
                logo=_feed.image.href,
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
            print("feed obj: ", feed_obj)
            return feed_obj
        except Exception as e:
            raise e
            # Handle the exception according to your requirements
            print(f"Error saving feed: {str(e)}")
            return None

    def fetch_and_save_feed(self):
        feed = self.fetch_feed()
        print("feed:", feed)
        if feed:
            return self._save_feed(feed)
        else:
            return None
