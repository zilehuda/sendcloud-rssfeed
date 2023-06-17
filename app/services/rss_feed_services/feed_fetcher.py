from typing import Optional
from fastapi import HTTPException
import feedparser
from feedparser import FeedParserDict
import logging

logger = logging.getLogger(__name__)


class RSSFeedFetcher:
    def __init__(self, feed_url: str) -> dict:
        self._feed_url = feed_url

    """
    Not implemented any retry mechanism, even on wrong url, it return data
    with empty entries.
    raise exception on wrong url on bozo
    """

    def fetch_feed(self) -> Optional[FeedParserDict]:
        logger = logging.getLogger(__name__)
        logger.info("Fetching feed from URL: %s", self._feed_url)

        feed = feedparser.parse(self._feed_url)

        if "bozo" in feed and feed["bozo"]:
            logger.error("Invalid RSS feed provided: %s", self._feed_url)
            raise HTTPException(
                status_code=400, detail="The RSS feed provided is invalid."
            )

        logger.info("Feed fetched successfully.")
        return feed
