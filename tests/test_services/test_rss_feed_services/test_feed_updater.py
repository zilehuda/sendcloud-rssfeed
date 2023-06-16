from datetime import datetime, timezone
from time import mktime
from unittest.mock import patch

from feedparser import FeedParserDict
from sqlalchemy.orm import Session

from app.constants import FetchStatus
from app.models import Feed, Post
from app.services.rss_feed_services import RSSFeedUpdater
from tests.factories import FeedFactory
from tests.mock_responses import mock_rss_feed_response


@patch("app.services.rss_feed_services.feed_updater.RSSFeedFetcher.fetch_feed")
def test_fetch_and_update_feed(mock_fetcher, db_session):
    # Create a mock feed object
    feed_id = 1
    feed_url = "https://example.com/feed"
    feed_obj = FeedFactory(id=feed_id, feed_url=feed_url, latest_post_id="123")

    # Create a mock feed parser response
    mock_feed_entries = [
        {
            "id": "456",
            "title": "Entry 1",
            "summary": "Summary of Entry 1",
            "author": "John Doe",
            "link": "https://example.com/entry1",
            "published_parsed": (2023, 6, 15, 0, 0, 0, 0, 0, 0),
        },
    ]
    mock_rss_feed_response["entries"] = mock_feed_entries

    # Configure the mock fetch feed function to return the mock feed response
    mock_fetcher.return_value = mock_rss_feed_response

    # Create an instance of the RSSFeedUpdater
    updater = RSSFeedUpdater(db_session, feed_id)

    # Call the fetch_and_update_feed method
    updater.fetch_and_update_feed()

    # Check that the fetch_feed method was called with the correct URL
    mock_fetcher.assert_called_once_with()

    # Check that the feed entries were updated in the database
    assert len(db_session.query(Post).all()) == len(mock_feed_entries)

    # Check that the latest_post_id and fetch_status were updated in the Feed table
    updated_feed = db_session.get(Feed, feed_id)
    assert updated_feed.latest_post_id == "456"
    assert updated_feed.fetch_status == FetchStatus.COMPLETED.value
