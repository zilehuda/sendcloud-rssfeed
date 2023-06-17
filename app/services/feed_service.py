import logging
from typing import Optional, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import tasks as app_tasks
from app.constants import FetchStatus
from app.models import Feed, User
from app.repositories.feed_repository import FeedRepository
from app.repositories.user_repository import UserRepository
from app import schemas

logger = logging.getLogger(__name__)


def get_feeds_for_user(
    db: Session, user: User, skip: int = 0, limit: int = 10
) -> list[Feed]:
    logger.info(f"Retrieving feeds for user {user.id} from skip={skip}, limit={limit}")
    feed_repository = FeedRepository(db)
    feeds: list[Feed] = feed_repository.get_feeds(skip, limit)

    # Determine if the user is following each feed
    feed_ids_followed = set(feed.id for feed in user.feeds)
    for feed in feeds:
        feed.followed = feed.id in feed_ids_followed

    logger.info(f"Retrieved {len(feeds)} feeds")
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

    logger.info(f"User {user.id} started following feed {feed_id}")


def unfollow_feed(db: Session, user: User, feed_id: int) -> None:
    feed_repository = FeedRepository(db)
    feed: Feed = feed_repository.get_feed_by_id(feed_id)

    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed not in user.feeds:
        raise HTTPException(status_code=400, detail="You are not following this feed")

    user_repository = UserRepository(db)
    user_repository.remove_feed_from_user(user, feed)

    logger.info(f"User {user.id} unfollowed feed {feed_id}")


def create_feed_from_url_for_user(
    db: Session, user: User, feed_url: str
) -> Tuple[Optional[str], str]:
    feed_repository = FeedRepository(db)
    feed = feed_repository.get_feed_by_feed_url(feed_url)

    if feed:
        # Feed already exists
        user_feeds_ids = set(feed.id for feed in user.feeds)
        if feed.id not in user_feeds_ids:
            user_repository = UserRepository(db)
            user_repository.add_feed_to_user(user, feed)

        logger.info(f"User {user.id} started following feed from URL: {feed_url}")
        return None, "User started following the feed"

    task = app_tasks.fetch_and_assign_feed_to_user.delay(user.id, feed_url)
    logger.info(
        f"Fetching the feed from URL: {feed_url} has been started for user {user.id}"
    )

    return task.id, "Fetching the feed has been started"


def force_refresh_feed(
    db: Session, user: User, feed_id: int
) -> Tuple[Optional[str], str]:
    feed_repository = FeedRepository(db)
    feed: Feed = feed_repository.get_feed_by_id(feed_id)

    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed not in user.feeds:
        raise HTTPException(status_code=400, detail="You are not following this feed")

    if feed.fetch_status == FetchStatus.RETRYING.value:
        return None, "The process of retrieving feed updates is currently in progress."

    task = app_tasks.force_refresh_feed.delay(feed.id)
    return task.id, "The update process for feeds has been initiated."


def change_feed_fetch_status(
    db: Session, feed_id: int, fetch_status: FetchStatus
) -> None:
    feed_repository = FeedRepository(db)
    feed: Feed = feed_repository.get_feed_by_id(feed_id)
    feed.fetch_status = fetch_status.value
    db.commit()
