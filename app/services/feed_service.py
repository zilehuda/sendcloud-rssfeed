from typing import Optional

from app.models import Feed, User
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.feed_repository import FeedRepository
from app.repositories.user_repository import UserRepository
from app.services.rss_feed_services import RSSFeedFetcher, RSSFeedCreator
from app.tasks import fetch_and_assign_feed_to_user


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

    user_repository = UserRepository(db)
    user_repository.add_feed_to_user(user, feed)


def unfollow_feed(db: Session, user: User, feed_id: int) -> None:
    feed_repository = FeedRepository(db)
    feed: Feed = feed_repository.get_feed_by_id(feed_id)

    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed not in user.feeds:
        raise HTTPException(status_code=400, detail="You are not following this feed")

    user_repository = UserRepository(db)
    user_repository.remove_feed_from_user(user, feed)


def create_feed_from_url_for_user(
    db: Session, user: User, feed_url: str
) -> (Optional[int], str):
    feed_repository = FeedRepository(db)
    feed = feed_repository.get_feed_by_feed_url(feed_url)

    if feed:
        # Feed already exists
        user_feeds_ids = set(feed.id for feed in user.feeds)
        if feed.id not in user_feeds_ids:
            user_repository = UserRepository(db)
            user_repository.add_feed_to_user(user, feed)

        return None, "User started following the feed"

    task = fetch_and_assign_feed_to_user.delay(user.id, feed_url)
    return task.id, "Fetching the feed has been started"
