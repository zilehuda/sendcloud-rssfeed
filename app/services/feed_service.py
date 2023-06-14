from app.models import Feed, User
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.feed_repository import FeedRepository


def get_feeds_for_user(db: Session, user: User, skip: int = 0, limit: int = 10):
    feed_repository = FeedRepository(db)
    feeds = feed_repository.get_feeds(skip, limit)

    # Determine if the user is following each feed
    feed_ids_followed = set(feed.id for feed in user.feeds)
    for feed in feeds:
        feed.followed = feed.id in feed_ids_followed

    return feeds


def follow_feed(db: Session, user: User, feed_id: int) -> None:
    feed_repository = FeedRepository(db)
    feed = feed_repository.get_feed_by_id(feed_id)

    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed in user.feeds:
        raise HTTPException(
            status_code=400, detail="You are already following this feed"
        )

    feed_repository.add_feed_to_user(user, feed)


def unfollow_feed(db: Session, user: User, feed_id: int) -> None:
    feed_repository = FeedRepository(db)
    feed = feed_repository.get_feed_by_id(feed_id)

    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed not in user.feeds:
        raise HTTPException(
            status_code=400, detail="You are already not following this feed"
        )

    feed_repository.remove_feed_from_user(user, feed)
