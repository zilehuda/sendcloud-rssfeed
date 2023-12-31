from tests.factories import FeedFactory, UserFactory


def test_get_feeds(bob_client):
    UserFactory()
    FeedFactory.create_batch(10)

    # Make a request to the get_feeds endpoint
    response = bob_client.get("/api/feeds")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["feeds"]) == 10


def test_follow_feed(bob_client):
    feed = FeedFactory.create()
    # Make a request to the get_feeds endpoint
    response = bob_client.post(f"/api/feeds/{feed.id}/follow")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Successfully followed the feed"


def test_unfollow_feed(bob_client, bob_user):
    # Create a feed and make Bob follow it
    feed = FeedFactory.create()
    # TODO: follow feed using factory
    bob_client.post(f"/api/feeds/{feed.id}/follow")

    # Make a request to unfollow the feed
    response = bob_client.delete(f"/api/feeds/{feed.id}/follow")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Successfully unfollowed the feed"
