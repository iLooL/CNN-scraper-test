import requests # for url requests
import feedparser

def getArticleURLs(URL):
    url = URL

    # get the RSS feed
    feed = feedparser.parse(url)
    # get all entries from feed
    entries = feed.entries
    # stores the urls for each article
    articles_urls = []

    for entry in entries:
        articles_urls.append(entry['link'])

    return articles_urls