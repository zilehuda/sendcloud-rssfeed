import feedparser
from feedparser import FeedParserDict
from typing import Optional


class RSSFeedFetcher:
    def __init__(self, feed_url: str) -> None:
        self.feed_url = feed_url

    def fetch_feed(self) -> Optional[FeedParserDict]:
        try:
            feed = feedparser.parse(self.feed_url)
            return feed
        except Exception as e:
            # Handle the exception according to your requirements
            print(f"Error fetching feed: {str(e)}")
            return None
