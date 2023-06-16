from unittest.mock import patch, MagicMock

from app.models import User
import pytest


def test_hello(bob_client):
    # Make a request to the get_feeds endpoint
    response = bob_client.get(f"/auth/hello")
    print(response.json())
    print(response.status_code)

    skip, limit = 0, 10
    response = bob_client.get(f"/api/posts?skip={skip}&limit={limit}")
    print(response.json())
    print(response.status_code)
