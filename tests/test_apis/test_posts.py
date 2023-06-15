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
    assert len(response_data["posts"]) == 10


def test_mark_post_as_read_unread(bob_client):
    feed = FeedFactory()
    post = PostFactory.create(feed=feed)

    # follow a feed, TODO: follow through factory
    bob_client.post(f"/api/feeds/{feed.id}/follow")

    # Make a request to mark the post as read
    response = bob_client.put(f"/api/posts/{post.id}/read?read=true")

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"message": "Post marked as read"}

    # Make a request to mark the post as unread
    response = bob_client.put(f"/api/posts/{post.id}/read?read=false")

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"message": "Post marked as unread"}
