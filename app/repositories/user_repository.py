from sqlalchemy.orm import Session

from app.models import Feed, User


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_user_by_id(self, user_id: int) -> User:
        return self._db.get(User, user_id)

    def get_user_by_email(self, email: str) -> User:
        return self._db.query(User).filter(User.email == email).first()

    def add_feed_to_user(self, user: User, feed: Feed) -> None:
        user.feeds.append(feed)
        self._db.commit()

    def remove_feed_from_user(self, user: User, feed: Feed) -> None:
        user.feeds.remove(feed)
        self._db.commit()

    def create_user(self, user: User) -> None:
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
