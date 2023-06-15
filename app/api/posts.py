from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.auth.service import get_current_user
from app.models import User
from sqlalchemy import event

from app.schemas import GetPostsResponse
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


@router.put("/{post_id}/read")
async def mark_post_as_read_unread(
    post_id: int,
    read: bool,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_read_posts_ids = set(post.id for post in user.read_posts)
    message: str = ""
    if read:
        # Mark post as read
        if post.id not in user_read_posts_ids:
            user.read_posts.append(post)
        message = "Post marked as read"
    else:
        # Mark post as unread
        if post.id in user_read_posts_ids:
            user.read_posts.remove(post)
        message = "Post marked as unread"

    db.commit()
    db.refresh(post)
    return {"message": message}
