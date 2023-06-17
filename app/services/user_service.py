from sqlalchemy.orm import Session

from app.models import Feed
from app.repositories.user_repository import UserRepository


def assign_feed_to_user(db: Session, user_id: int, feed: Feed) -> None:
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_id(user_id)
    user_repository.add_feed_to_user(user, feed)
