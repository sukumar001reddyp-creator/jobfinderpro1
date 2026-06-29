import feedparser


class RSSClient:

    def fetch(self, url):

        feed = feedparser.parse(url)

        return feed.entries