from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Post, User
from app.utils.base_repository import BaseRepository


class PostRepository(BaseRepository):
    def get_posts_by_filter(
        self,
        skip: int,
        limit: int,
        read: Optional[bool],
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

    def mark_post_as_read(self, user: User, post: Post) -> None:
        user.read_posts.append(post)
        self._db.commit()

    def mark_post_as_unread(self, user: User, post: Post) -> None:
        user.read_posts.remove(post)
        self._db.commit()

    def get_post_by_id(self, post_id: int) -> Post:
        return self._db.get(Post, post_id)

    def create_posts(self, posts: list[Post]) -> None:
        self._db.add_all(posts)
        self._db.commit()
