from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.repositories.post_repository import PostRepository


def get_posts_for_user_by_filter(
    db: Session,
    user: User,
    feed_id: int,
    skip: int = 0,
    limit: int = 10,
    read: Optional[None] = None,
):
    # TODO: need to optimize the queries
    followed_feed_ids = [feed.id for feed in user.feeds]

    if len(followed_feed_ids) == 0:
        return []

    if feed_id and feed_id not in set(followed_feed_ids):
        raise HTTPException(
            status_code=403, detail="User is not following the specified feed"
        )

    if feed_id:
        followed_feed_ids = [feed_id]

    user_read_posts_ids = set(post.id for post in user.read_posts)

    post_repository = PostRepository(db)

    posts = post_repository.get_posts_by_filter(
        user,
        skip,
        limit,
        read,
        feed_id,
        followed_feed_ids,
        user_read_posts_ids,
    )
    for post in posts:
        post.is_read = post.id in user_read_posts_ids

    return posts


def change_post_read_status(db: Session, user: User, post_id: int, read: bool) -> str:
    post_repository = PostRepository(db)
    post = post_repository.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_read_posts_ids = set(post.id for post in user.read_posts)
    if read:
        # Mark post as read
        if post.id not in user_read_posts_ids:
            post_repository.mark_post_as_read(user, post)
        message = "Post marked as read"
    else:
        # Mark post as unread
        if post.id in user_read_posts_ids:
            post_repository.mark_post_as_unread(user, post)
        message = "Post marked as unread"

    return message
