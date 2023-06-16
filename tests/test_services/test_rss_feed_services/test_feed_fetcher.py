from unittest.mock import patch
from fastapi import HTTPException
from app.services.rss_feed_services.feed_fetcher import RSSFeedFetcher
import pytest


def test_fetch_feed(mock_feedparser_parse):
    # Create an instance of RSSFeedFetcher and call fetch_feed
    feed_url = "https://example.com/feed"
    fetcher = RSSFeedFetcher(feed_url)
    result = fetcher.fetch_feed()

    # Assert that the mock parse function was called with the correct URL
    mock_feedparser_parse.assert_called_once_with(feed_url)
    assert isinstance(result, dict)
    # Assert that the result matches the expected feed data
    assert result["feed"]["title"] == "Example Feed"
    assert len(result.get("entries")) == 2

    assert (
        mock_feedparser_parse.call_count == 1
    )  # Additional calls to mock_parse were not made


@patch("app.services.rss_feed_services.feed_fetcher.feedparser.parse")
def test_fetch_feed_invalid(mock_parse):
    # Mock the feedparser.parse function to simulate an invalid feed
    mock_feed = {"bozo": True}
    mock_parse.return_value = mock_feed

    # Create an instance of RSSFeedFetcher and call fetch_feed
    feed_url = "https://example.com/invalid-feed"
    fetcher = RSSFeedFetcher(feed_url)

    # Assert that an HTTPException is raised with the correct status code and detail
    with pytest.raises(HTTPException) as exc_info:
        fetcher.fetch_feed()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The RSS feed provided is invalid."
