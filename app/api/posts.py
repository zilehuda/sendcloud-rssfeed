from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import GetPostsResponse, ResponseWithMessage
from app.services import post_service

router = APIRouter()


@router.get("", response_model=GetPostsResponse)
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    read: Optional[bool] = None,
    feed_id: Optional[int] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetPostsResponse:
    posts = post_service.get_posts_for_user_by_filter(
        db, user, feed_id, skip, limit, read
    )
    return GetPostsResponse(posts=posts)


@router.put("/{post_id}/read", response_model=ResponseWithMessage)
async def mark_post_as_read_unread(
    post_id: int,
    read: bool,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResponseWithMessage:
    message = post_service.change_post_read_status(db, user, post_id, read)
    return ResponseWithMessage(message=message)
