import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import User, Feed, Post
from testdbconfig import TestingSessionLocal

db = TestingSessionLocal()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    password = factory.Faker("password")

    @factory.post_generation
    def read_posts(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for post in extracted:
                UserFeedFactory.create(user=self, post=post)


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

    @factory.post_generation
    def read_by_users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.read_by_users.append(user)


# Factory for user_feeds relationship
class UserFeedFactory(factory.Factory):
    class Meta:
        model = None

    user = factory.SubFactory(UserFactory)
    feed = factory.SubFactory(FeedFactory)


# Factory for user_post_read relationship
class UserPostReadFactory(factory.Factory):
    class Meta:
        model = None

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
