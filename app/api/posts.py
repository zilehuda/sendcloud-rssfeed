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
    if feed_id is None:
        query = query.filter(Post.feed_id.in_(followed_feed_ids))
    else:
        if feed_id not in followed_feed_ids:
            raise HTTPException(
                status_code=403, detail="User is not following the specified feed"
            )
        query = query.filter(Post.feed_id == feed_id)

    if read is not None:
        # Filter based on read/unread status
        if read:
            # Fetch read posts
            query = query.filter(Post.id.in_([post.id for post in user.posts_read]))
        else:
            # Fetch unread posts
            query = query.filter(~Post.id.in_([post.id for post in user.posts_read]))

    query = query.order_by(desc(Post.published_at))
    posts = query.offset(skip).limit(limit).all()

    # Fetch the read status for each post
    post_ids = [post.id for post in posts]
    post_read_status = {
        post_id: post_id in [post.id for post in user.posts_read]
        for post_id in post_ids
    }
    # Create a dictionary representation of each post with read status
    formatted_posts = [
        {
            "id ": post.id,
            "title": post.title,
            "summary": post.summary,
            "author": post.author,
            "post_url": post.post_url,
            "feed_id": post.feed_id,
            "published_at": post.published_at,
            "is_read": post_read_status.get(post.id, False),
        }
        for post in posts
    ]
    return formatted_posts


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

    if read:
        # Mark post as read
        if post not in user.posts_read:
            user.posts_read.append(post)
    else:
        # Mark post as unread
        if post in user.posts_read:
            user.posts_read.remove(post)

    db.commit()
    return {"message": "Read status has been updated"}
