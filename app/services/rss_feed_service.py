from datetime import datetime, timezone
from time import mktime

import feedparser
from feedparser import FeedParserDict
from sqlalchemy.orm import Session

from app.models import Feed, Post
from typing import Optional


class RssFeedFetcher:
    def __init__(self, feed_url: str) -> None:
        self.feed_url = feed_url

    def fetch_feed(self) -> Optional[FeedParserDict]:
        try:
            feed = feedparser.parse(self.feed_url)
            return feed
        except Exception as e:
            # Handle the exception according to your requirements
            print(f"Error fetching feed: {str(e)}")
            return None


class RSSFeedCreator:
    def __init__(self, feed_url: str, fetcher: RssFeedFetcher, db: Session) -> None:
        self.feed_url = feed_url
        self._db = db
        self._fetcher = fetcher

    def _save_feed(self, feed: FeedParserDict) -> Feed:
        try:
            _feed = feed.feed
            latest_post_id: Optional[str] = None
            if len(feed.entries):
                latest_post_id = feed.entries[0].id

            feed_obj: Feed = Feed(  # type: ignore[misc]
                title=_feed.title,
                website=_feed.link,
                feed_url=self.feed_url,
                logo=_feed.image.href,
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


class RSSFeedUpdater:
    def __init__(self, feed_id: int, fetcher: RssFeedFetcher, db: Session) -> None:
        self.feed_id = feed_id
        self._fetcher = fetcher
        self._db = db

    def _update_feed(self, feed_obj: Feed, feed_entries: FeedParserDict) -> None:
        try:
            latest_post_id = feed_obj.latest_post_id
            for entry in feed_entries:
                if latest_post_id and entry.id == latest_post_id:
                    break
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
                    feed_id=feed_obj.id,
                )
                self._db.add(post_obj)

            if len(feed_entries) > 0:
                latest_post_id = feed_entries[0].id

            # Update the latest_post_id in the Feed table
            feed_obj.latest_post_id = latest_post_id
            self._db.commit()

            print("Feed entries updated successfully.")
        except Exception as e:
            raise e
            # Handle the exception according to your requirements
            print(f"Error saving feed entries: {str(e)}")

    def fetch_and_update_feed(self) -> None:
        feed_obj: Optional[Feed] = self._db.query(Feed).get(self.feed_id)
        if feed_obj is None:
            raise ValueError(f"Feed with ID {self.feed_id} does not exist.")

        fetched_feed: FeedParserDict = self._fetcher.fetch_feed()
        if fetched_feed:
            self._update_feed(
                feed_obj,
                fetched_feed.entries,
            )
