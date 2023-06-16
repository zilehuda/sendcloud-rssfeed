from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.feed_service as feed_service
from app.auth.service import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import (GetFeedsResponse, ResponseWithMessage,
                         ResponseWithTaskIdAndMessage)

router = APIRouter()


@router.get("", response_model=GetFeedsResponse)
async def get_feeds(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetFeedsResponse:
    feeds = feed_service.get_feeds_for_user(db, user, skip, limit)
    return GetFeedsResponse(feeds=feeds)


@router.post("/")
async def create_feed(
    feed_url: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ "
    TODO: No validation or cleaning yet on feed_url, suppose to get the
    accurate feed_url.
    TODO: Response and everything could be improve more
    """
    task, message = feed_service.create_feed_from_url_for_user(db, user, feed_url)
    return {
        "task": task,
        "message": message,
    }


@router.post("/{feed_id}/follow", response_model=ResponseWithMessage)
def follow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithMessage:
    feed_service.follow_feed(db, user, feed_id)
    return ResponseWithMessage(message="Successfully followed the feed")


@router.delete("/{feed_id}/follow", response_model=ResponseWithMessage)
async def unfollow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithMessage:
    feed_service.unfollow_feed(db, user, feed_id)
    return ResponseWithMessage(message="Successfully unfollowed the feed")


"""
NOTE: If a user performs a force refresh on a feed, 
the updated posts from that feed will be visible to all users.
"""


@router.post("/{feed_id}/force-refresh", response_model=ResponseWithTaskIdAndMessage)
async def force_refresh_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResponseWithTaskIdAndMessage:
    task_id, message = feed_service.force_refresh_feed(db, user, feed_id)
    return ResponseWithTaskIdAndMessage(task_id=task_id, message=message)
