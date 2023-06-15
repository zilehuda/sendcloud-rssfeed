from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.database import get_db
from app.models import User

from app.schemas import GetFeedsResponse, ResponseWithMessage
import app.services.feed_service as feed_service
from app.config import get_settings, Settings
from typing import Annotated

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
