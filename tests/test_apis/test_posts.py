from tests.factories import FeedFactory, PostFactory


def test_get_posts(bob_client):
    feed = FeedFactory()
    PostFactory.create_batch(12, feed=feed)

    # follow a feed, TODO: follow through factory
    bob_client.post(f"/api/feeds/{feed.id}/follow")

    skip, limit = 0, 10
    response = bob_client.get(f"/api/posts?skip={skip}&limit={limit}")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 10
