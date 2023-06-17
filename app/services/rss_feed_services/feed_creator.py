from datetime import datetime, timezone
from time import mktime
from typing import Optional

from feedparser import FeedParserDict
from sqlalchemy.orm import Session

from app.models import Feed, Post

from .feed_fetcher import RSSFeedFetcher
from app.repositories.feed_repository import FeedRepository

import logging

logger = logging.getLogger(__name__)


class RSSFeedCreator:
    def __init__(self, db: Session, feed_url: str) -> None:
        logger.info("Initializing RSSFeedCreator")
        self.feed_url = feed_url
        self._db = db
        self._fetcher = RSSFeedFetcher(self.feed_url)

    def _save_feed(self, feed: FeedParserDict) -> Feed:
        try:
            logger.info("Saving feed")
            _feed = feed["feed"]
            latest_post_id: Optional[str] = None
            if len(feed["entries"]):
                latest_post_id = feed["entries"][0]["id"]

            logo: str = ""
            if "image" in _feed:
                logo = _feed["image"]["href"]
            elif "logo" in _feed:
                logo = _feed["logo"]

            # Create a Feed object
            feed_obj: Feed = Feed(  # type: ignore[misc]
                title=_feed["title"],
                website=_feed["link"],
                feed_url=self.feed_url,
                logo=logo,
                latest_post_id=latest_post_id,
            )

            post_objs: list[Post] = []
            for entry in feed["entries"]:
                # Create a Post object for each entry in the feed
                post_obj = Post(
                    post_id=entry["id"],
                    title=entry["title"],
                    summary=entry["summary"],
                    author=entry["author"],
                    post_url=entry["link"],
                    published_at=datetime.fromtimestamp(
                        mktime(entry["published_parsed"]),
                        timezone.utc,
                    ),
                    feed=feed_obj,
                )
                post_objs.append(post_obj)

            # Create a FeedRepository instance and save the feed with its posts
            feed_repository = FeedRepository(self._db)
            feed_repository.create_feed_with_posts(feed_obj, post_objs)
            logger.info("Feed saved successfully")
            return feed_obj
        except Exception as e:
            logger.error(f"Error occurred while saving feed: {str(e)}")
            raise e

    def fetch_and_save_feed(self) -> Optional[Feed]:
        try:
            logger.info("Fetching and saving feed")
            existing_feed = (
                self._db.query(Feed).filter_by(feed_url=self.feed_url).first()
            )
            if existing_feed:
                logger.info("Feed already exists")
                return existing_feed
            else:
                # Fetch the feed using the RSSFeedFetcher
                feed = self._fetcher.fetch_feed()
                if feed:
                    logger.info("Feed fetched successfully")
                    return self._save_feed(feed)  # Save the fetched feed
                else:
                    logger.error("Error occurred while fetching the feed.")
                    return None
        except Exception as e:
            logger.error(f"Error occurred while fetching and saving feed: {str(e)}")
            raise e
