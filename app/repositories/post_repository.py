from sqlalchemy.orm import Session
from typing import List
from app.models import Post, User
from typing import Optional
from sqlalchemy import desc


class PostRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_posts_by_filter(
        self,
        user: User,
        skip: int,
        limit: int,
        read: Optional[bool],
        feed_id: Optional[int],
        followed_feed_ids: Optional[list[int]],
        user_read_posts_ids: Optional[list[int]],
    ):
        query = self._db.query(Post)
        query = query.filter(Post.feed_id.in_(followed_feed_ids))

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

        return posts

    def get_feed_by_id(self, post_id: int) -> Post:
        return self._db.query(Post).get(post_id)
