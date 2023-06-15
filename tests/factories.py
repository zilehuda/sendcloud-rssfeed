import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import User, Feed, Post, UserPostRead, UserFeed
from testdbconfig import TestingSessionLocal

db = TestingSessionLocal()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    password = factory.Faker("password")


class FeedFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Feed
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("sentence")
    feed_url = factory.Faker("url")
    website = factory.Faker("url")
    logo = factory.Faker("image_url")


class PostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    post_id = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    summary = factory.Faker("text")
    author = factory.Faker("name")
    post_url = factory.Faker("url")
    published_at = factory.Faker("date_time_this_decade")
    feed = factory.SubFactory(FeedFactory)
