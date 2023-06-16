from typing import Optional

from sqlalchemy.orm import Session

from app.models import Feed, Post
from app.utils.base_repository import BaseRepository


class FeedRepository(BaseRepository):
    def get_feeds(self, skip: int = 0, limit: int = 10) -> list[Feed]:
        feeds = self._db.query(Feed).offset(skip).limit(limit).all()
        return feeds

    def get_feed_by_id(self, feed_id: int) -> Feed:
        return self._db.get(Feed, feed_id)

    def get_feed_by_feed_url(self, feed_url: str) -> Optional[Feed]:
        return self._db.query(Feed).filter_by(feed_url=feed_url).first()

    def create_feed_with_posts(self, feed: Feed, posts: list[Post]) -> None:
        self._db.add(feed)
        self._db.add_all(posts)
        self._db.commit()
        self._db.refresh(feed)
