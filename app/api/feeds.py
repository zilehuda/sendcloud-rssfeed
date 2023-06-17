import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.feed_service as feed_service
from app.auth.service import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import (GetFeedsResponse, ResponseWithMessage,
                         ResponseWithTaskIdAndMessage)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("", response_model=GetFeedsResponse)
async def get_feeds(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetFeedsResponse:
    logger.info("Get feeds request received")
    feeds = feed_service.get_feeds_for_user(db, user, skip, limit)
    logger.info("Feeds fetched successfully")
    return GetFeedsResponse(feeds=feeds)


@router.post("/", response_model=ResponseWithTaskIdAndMessage)
async def create_feed(
    feed_url: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResponseWithTaskIdAndMessage:
    """ "
    TODO: No validation or cleaning yet on feed_url, suppose to get the
    accurate feed_url.
    """
    logger.info(f"Create feed request received. feed_url={feed_url}")
    task_id, message = feed_service.create_feed_from_url_for_user(db, user, feed_url)
    logger.info(f"Feed created with task={task_id}, message={message}")
    return ResponseWithTaskIdAndMessage(task_id=task_id, message=message)


@router.post("/{feed_id}/follow", response_model=ResponseWithMessage)
def follow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithMessage:
    logger.info(f"Follow feed request received. feed_id={feed_id}")
    feed_service.follow_feed(db, user, feed_id)
    logger.info("Successfully followed the feed")
    return ResponseWithMessage(message="Successfully followed the feed")


@router.delete("/{feed_id}/follow", response_model=ResponseWithMessage)
async def unfollow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithMessage:
    logger.info(f"Unfollow feed request received. feed_id={feed_id}")
    feed_service.unfollow_feed(db, user, feed_id)
    logger.info("Successfully unfollowed the feed")
    return ResponseWithMessage(message="Successfully unfollowed the feed")


@router.post("/{feed_id}/force-refresh", response_model=ResponseWithTaskIdAndMessage)
async def force_refresh_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithTaskIdAndMessage:
    """
    NOTE: If a user performs a force refresh on a feed,
    the updated posts from that feed will be visible to all users.
    """
    logger.info(f"Force refresh feed request received. feed_id={feed_id}")
    task_id, message = feed_service.force_refresh_feed(db, user, feed_id)
    logger.info(
        f"Force refresh feed completed with task_id={task_id}, message={message}"
    )
    return ResponseWithTaskIdAndMessage(task_id=task_id, message=message)
