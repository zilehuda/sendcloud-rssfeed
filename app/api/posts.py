import logging
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import GetPostsResponse, ResponseWithMessage
from app.services import post_service

logger = logging.getLogger(__name__)

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
    logger.info(f"Get posts request received.")
    posts = post_service.get_posts_for_user_by_filter(
        db, user, feed_id, skip, limit, read
    )
    logger.info("Posts received successful")
    return GetPostsResponse(posts=posts)


@router.put("/{post_id}/read", response_model=ResponseWithMessage)
async def mark_post_as_read_unread(
    post_id: int,
    read: bool,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResponseWithMessage:
    logger.info(
        f"User {user.id} is marking post {post_id} as {'read' if read else 'unread'}"
    )
    message = post_service.change_post_read_status(db, user, post_id, read)
    logger.info(
        f"Post {post_id} marked as {'read' if read else 'unread'} for user {user.id}"
    )
    return ResponseWithMessage(message=message)
