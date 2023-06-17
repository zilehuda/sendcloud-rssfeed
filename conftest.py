from fastapi.testclient import TestClient
from app.auth.jwt_handler import create_access_token
from app.database import Base, get_db
from app.main import app as main_app
import pytest
from unittest.mock import patch
from app.models import User
from testdbconfig import engine, TestingSessionLocal
from tests.factories import UserFactory
from app.auth.service import get_current_user
from tests.mock_responses import mock_rss_feed_response


@pytest.fixture(scope="function")
def test_app():
    Base.metadata.create_all(bind=engine)  # Create the tables.
    yield main_app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_app):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def override_dependencies(test_app, db_session):
    test_app.dependency_overrides[get_db] = override_get_db
    yield
    del test_app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def client(override_dependencies):
    with TestClient(main_app) as client:
        yield client


@pytest.fixture(scope="function")
def bob_user(test_app):
    return UserFactory.create(email="bob@thebuilder.com")


@pytest.fixture()
def bob_client(override_dependencies, bob_user):
    # TODO: better approach could be override get_curent_user
    access_token = create_access_token({"id": bob_user.id, "email": bob_user.email})
    client = TestClient(main_app, headers={"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture
def mock_feedparser_parse():
    with patch("app.services.rss_feed_services.feed_fetcher.feedparser.parse") as mock:
        # Mock the return value of the parse function
        mock.return_value = mock_rss_feed_response
        yield mock
