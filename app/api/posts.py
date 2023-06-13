from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.auth.service import get_current_user
from app.models import User
from sqlalchemy import event

router = APIRouter()


@router.get("")
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    read: Optional[bool] = None,
    feed_id: Optional[int] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # TODO: need to optimize the queries
    query = db.query(Post)

    followed_feed_ids = [feed.id for feed in user.feeds]

    if len(followed_feed_ids) == 0:
        return []

    if feed_id is None:
        query = query.filter(Post.feed_id.in_(followed_feed_ids))
    else:
        if feed_id not in followed_feed_ids:
            raise HTTPException(
                status_code=403, detail="User is not following the specified feed"
            )
        query = query.filter(Post.feed_id == feed_id)

    user_read_posts_ids = [post.id for post in user.read_posts]
    if read is not None:
        # Filter based on read/unread status
        if read:
            # Fetch read posts
            query = query.filter(Post.id.in_(user_read_posts_ids))
        else:
            # Fetch unread posts
            query = query.filter(~Post.id.in_(user_read_posts_ids))

    query = query.order_by(desc(Post.published_at))
    posts = query.offset(skip).limit(limit).all()

    user_read_posts_ids = set(user_read_posts_ids)
    for post in posts:
        post.is_read = post.id in user_read_posts_ids

    return posts


@router.put("/{post_id}/read")
async def mark_post_as_read_unread(
    post_id: int,
    read: bool = True,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_read_posts_ids = set(post.id for post in user.read_posts)
    if read:
        # Mark post as read
        if post.id not in user_read_posts_ids:
            user.read_posts.append(post)
    else:
        # Mark post as unread
        if post.id in user_read_posts_ids:
            user.read_posts.remove(post)

    db.commit()
    db.refresh(post)
    return {"message": "Read status has been updated"}
