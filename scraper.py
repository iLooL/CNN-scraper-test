from bs4 import BeautifulSoup
import requests
from RSSfeed import getArticleURLs

url = 'https://www.cbc.ca/cmlink/rss-politics'

# get all article links
response = getArticleURLs(url)

# take first article
first_article_url = response[0]
# remove rss URL ending
first_article_url = first_article_url.replace('?cmp=rss', '')

# request first webpage
html = requests.get(first_article_url)
    
soup = BeautifulSoup(html.content, 'lxml')

# get story contents, title and author
story_content = soup.find('div', {'class': 'story'}).find_all('p')
story_title = soup.find('h1', {'class': 'detailHeadline'}).text
story_author = soup.find('span', {'class': 'authorText'}).find('a').text

# story variable will have special characters
story = ''

for paragraph in story_content:
    story += paragraph.text
    story += '. '
