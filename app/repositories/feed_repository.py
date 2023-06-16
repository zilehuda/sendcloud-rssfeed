from typing import Optional

from sqlalchemy.orm import Session

from app.models import Feed


class FeedRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_feeds(self, skip: int = 0, limit: int = 10) -> list[Feed]:
        feeds = self._db.query(Feed).offset(skip).limit(limit).all()
        return feeds

    def get_feed_by_id(self, feed_id: int) -> Feed:
        return self._db.get(Feed, feed_id)

    def get_feed_by_feed_url(self, feed_url: str) -> Optional[Feed]:
        return self._db.query(Feed).filter_by(feed_url=feed_url).first()
