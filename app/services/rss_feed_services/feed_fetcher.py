import logging
from typing import Optional

import feedparser
from fastapi import HTTPException
from feedparser import FeedParserDict

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
        logger.info(f"Fetching feed from URL: {self._feed_url}")

        feed = feedparser.parse(self._feed_url)

        if "bozo" in feed and feed["bozo"]:
            logger.error(f"Invalid RSS feed provided: {self._feed_url}")
            raise HTTPException(
                status_code=400, detail="The RSS feed provided is invalid."
            )

        logger.info("Feed fetched successfully.")
        return feed
