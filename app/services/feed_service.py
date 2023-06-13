from abc import abstractmethod


class FeedService:
    def __init__(self, feed_url):
        self.feed_url = feed_url

    @abstractmethod
    def fetch_feed(self) -> None:
        raise NotImplementedError("Please implement fetch_feed method.")
