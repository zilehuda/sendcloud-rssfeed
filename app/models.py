from __future__ import annotations
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy_utils import EmailType, URLType

from app.database import Base
from app.utils.base_model import BaseModel

user_feeds = Table(
    "user_feeds",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("feed_id", ForeignKey("feeds.id"), primary_key=True),
)

user_post_read = Table(
    "user_post_read",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"
    email = Column(EmailType, unique=True)
    password = Column(String)
    feeds: Mapped[list[Feed]] = relationship(
        "Feed", secondary=user_feeds, back_populates="users"
    )
    posts_read = relationship(
        "Post", secondary=user_post_read, back_populates="read_by_users"
    )


class Feed(BaseModel):
    __tablename__ = "feeds"
    title = Column(String)
    feed_url = Column(URLType)
    website = Column(URLType)
    logo = Column(URLType)
    users: Mapped[list[User]] = relationship(
        "User", secondary=user_feeds, back_populates="feeds"
    )


class Post(BaseModel):
    __tablename__ = "posts"
    post_id = Column(String, unique=True)
    title = Column(String)
    summary = Column(Text)
    author = Column(String)
    post_url = Column(URLType)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    published_at = Column(DateTime)

    feed = relationship("Feed", backref="posts")
    read_by_users = relationship(
        "User", secondary=user_post_read, back_populates="posts_read"
    )
