from sqlalchemy.orm import Session
from typing import List
from app.models import Feed, User


class FeedRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_feeds(self, skip: int = 0, limit: int = 10) -> list[Feed]:
        feeds = self._db.query(Feed).offset(skip).limit(limit).all()
        return feeds

    def get_feed_by_id(self, feed_id: int) -> Feed:
        return self._db.get(Feed, feed_id)

    def add_feed_to_user(self, user: User, feed: Feed) -> None:
        user.feeds.append(feed)
        self._db.commit()

    def remove_feed_from_user(self, user: User, feed: Feed) -> None:
        user.feeds.remove(feed)
        self._db.commit()
