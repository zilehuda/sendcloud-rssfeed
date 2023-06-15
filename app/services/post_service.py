from app.models import Feed, User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.post_repository import PostRepository
from typing import Optional


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
