import requests # for url requests
import feedparser

def getArticleURLs(URL):
    """[summary]
    
    Arguments:
        URL [string] -- RSS url that you want to get all links from
    
    Returns:
        articles_urls [list] -- returns a list of all URLS found in RSS feed
    """
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