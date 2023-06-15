from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.jwt_handler import create_access_token
from app.database import Base, get_db
from app.main import app as main_app
import pytest
from testdbconfig import engine, TestingSessionLocal
from tests.factories import UserFactory


@pytest.fixture()
def bob_user():
    return UserFactory(email="bob@thebuilder.com")


@pytest.fixture(scope="function")
def test_app():
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(bind=engine)  # Create the tables.
    yield main_app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_app):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session  # use the session in tests.
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
    client = TestClient(main_app)
    yield client


@pytest.fixture()
def bob_client(override_dependencies, bob_user):
    access_token = create_access_token({"id": bob_user.id, "email": bob_user.email})
    client = TestClient(main_app, headers={"Authorization": f"Bearer {access_token}"})
    yield client
