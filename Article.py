from RSSfeed import getArticleURLs
from scraper import RSS_Scraper

"""
    Returns a list of articles from an RSS feed

    Each entry is an Article object
"""


class RSS_Articles:
    def __init__(self, url):
        """
            Takes URL of entire RSS feed, is a list of Article objects
        
        Arguments:
            url [string] -- RSS feed URL
        
        Returns:
            [RSS_Articles Object] -- object that contains all articles from 
            that RSS feed topic, ie. "https://www.cbc.ca/cmlink/rss-politics"
            will return all articles from that link
        """
        # gives us all article urls
        urls = getArticleURLs(url)
        self.articles = []

        # for url in urls:
        #     new_article = Article(url)
        #     self.articles.append(new_article)
        new_article = Article(urls[15])
        self.articles.append(new_article)



class Article:
    def __init__(self, url):
        title, author, full_text = RSS_Scraper(url)
        self.title = title
        self.author = author
        self.full_text = full_text


if __name__ == "__main__":
    url = "https://www.cbc.ca/cmlink/rss-politics"
    articles = RSS_Articles(url)
    print(articles.articles[0].title)