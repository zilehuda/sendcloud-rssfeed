from unittest.mock import patch

from app.models import Feed
from app.services.rss_feed_services.feed_creator import RSSFeedCreator
from testdbconfig import TestingSessionLocal
from tests.mock_responses import mock_rss_feed_response


@patch("app.services.rss_feed_services.feed_creator.RSSFeedFetcher")
def test_fetch_and_save_feed(mock_fetcher, db_session):
    # Mock the RSSFeedFetcher instance and its fetch_feed method

    mock_fetcher_instance = mock_fetcher.return_value
    mock_fetcher_instance.fetch_feed.return_value = mock_rss_feed_response

    # Create a mock Session
    mock_session = TestingSessionLocal()

    # Create an instance of RSSFeedCreator and call fetch_and_save_feed
    feed_url = "https://example.com/feed"
    creator = RSSFeedCreator(mock_session, feed_url)
    result = creator.fetch_and_save_feed()

    # Assert that the fetch_feed method was called on the mock fetcher instance
    mock_fetcher_instance.fetch_feed.assert_called_once()

    # Assert the returned result
    assert isinstance(result, Feed)
    assert result.title == "Example Feed"
    assert len(result.posts) == 2

    assert (
        mock_fetcher.call_count == 1
    )  # Additional calls to mock_fetcher were not made
