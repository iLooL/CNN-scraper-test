from bs4 import BeautifulSoup
import re
import requests

def RSS_Scraper(URL):
    """
        Takes URL of RSS feed and returns the contents of a single article

    Arguments:
        URL [string] -- URL of RSS feed article, works on CBC
        Politics (maybe the others?) RSS feed

    Returns: All variables as strings
        story_title -- title of article
        story_author -- who authoured the content
        story -- the articles written content

    Todo:
        -story variable still has special characters
    """     
    # remove rss URL ending
    URL = URL.replace('?cmp=rss', '')

    # get html from url
    html = requests.get(URL)        
    soup = BeautifulSoup(html.content, 'lxml')

    # get story contents, title and author
    story_content = soup.find('div', {'class': 'story'}).find_all('p')
    story_title = soup.find('h1', {'class': 'detailHeadline'}).text

    try:
        story_author = soup.find('span', {'class': 'authorText'}).find('a').text
    except AttributeError as error:
        story_author = "NO AUTHOR"

    # story variable still has special characters
    story = ""

    for paragraph in story_content:
        story += paragraph.text
        story += " "

    return story_title, story_author, story
