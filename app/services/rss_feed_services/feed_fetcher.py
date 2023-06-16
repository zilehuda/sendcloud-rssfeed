from typing import Optional
from fastapi import HTTPException
import feedparser
from feedparser import FeedParserDict


class RSSFeedFetcher:
    def __init__(self, feed_url: str) -> None:
        self._feed_url = feed_url

    """
    Not implemented any retry mechanism, even on wrong url, it return data
    with empty entries.
    raise exception on wrong url on bozo
    """

    def fetch_feed(self) -> Optional[FeedParserDict]:
        feed = feedparser.parse(self._feed_url)
        if "bozo" in feed and feed.bozo:
            raise HTTPException(
                status_code=400, detail="The RSS feed provided is invalid."
            )
        return feed
