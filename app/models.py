from __future__ import annotations
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy_utils import EmailType, URLType

from app.constants import FetchStatus
from app.database import Base
from app.utils.base_model import BaseModel


class UserFeed(Base):
    __tablename__ = "user_feeds"
    user_id = Column("user_id", ForeignKey("users.id"), primary_key=True)
    feed_id = Column("feed_id", ForeignKey("feeds.id"), primary_key=True)


class UserPostRead(Base):
    __tablename__ = "user_post_read"
    user_id = Column("user_id", ForeignKey("users.id"), primary_key=True)
    post_id = Column("post_id", ForeignKey("posts.id"), primary_key=True)


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    email = Column(EmailType, unique=True)
    password = Column(String)
    feeds: Mapped[list[Feed]] = relationship(
        "Feed", secondary=UserFeed.__tablename__, back_populates="users"
    )
    read_posts = relationship(
        "Post", secondary=UserPostRead.__tablename__, back_populates="read_by_users"
    )


class Feed(BaseModel):
    __tablename__ = "feeds"
    id = Column(Integer(), primary_key=True)
    title = Column(String)
    feed_url = Column(URLType)
    website = Column(URLType)
    logo = Column(URLType)
    users: Mapped[list[User]] = relationship(
        "User", secondary=UserFeed.__tablename__, back_populates="feeds"
    )
    latest_post_id: None = Column(String, default=None, nullable=True)
    fetch_status = Column(
        String,
        default=FetchStatus.COMPLETED.value,
        nullable=False,
        server_default=FetchStatus.COMPLETED.value,
    )


class Post(BaseModel):
    __tablename__ = "posts"
    id = Column(Integer(), primary_key=True)
    post_id = Column(String, unique=True)
    title = Column(String)
    summary = Column(Text)
    author = Column(String)
    post_url = Column(URLType)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    published_at = Column(DateTime)

    feed = relationship("Feed", backref="posts")
    read_by_users = relationship(
        "User", secondary=UserPostRead.__tablename__, back_populates="read_posts"
    )
