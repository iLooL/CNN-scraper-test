from RSSfeed import getArticleURLs
from scraper import RSS_Scraper
import os
import nltk
import heapq
import json
import re

"""
    Returns a list of articles from an RSS feed

    Each entry is an Article object

    Todo:
        -remove blocks for all articles, it currently looks at only one
"""
def getArticleType(url):

    before, word, after = url.partition("-")
    print(before, word, after)

    return after

def summarize(article_text):

    # preprocess article_text

    # key is word, value is frequency of that word
    word_frequencies = {}

    # holds sentence ranking
    sentence_scores = {}

    # converts article text into sentences in an array
    # keys are sentences, values are importance score based on word frequency
    sentence_list = nltk.sent_tokenize(article_text)


    stopwords = nltk.corpus.stopwords.words('english')

    for word in nltk.word_tokenize(article_text):
        # words that aren't stopwords are important
        if word not in stopwords:
            if word not in word_frequencies.keys():
                # create that key
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        
    most_frequent = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / most_frequent)

    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                # is a summary, we dont want more than 30 words per sentence
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return summary

class RSS_Articles:
    def __init__(self, URL):
        """
            Takes URL of entire RSS feed, is a list of Article objects
        
        Arguments:
            url [string] -- RSS feed URL
        
        Returns:
            [RSS_Articles Object] -- object that contains all articles from 
            that RSS feed topic, ie. "https://www.cbc.ca/cmlink/rss-politics"
            will return all articles from that link
        """

        # add to topics list to retreive different topics from CBC RSS feed
        base = "/cmlink/rss-"
        topics = ["politics", "technology", "sports"]
        article_id = 1
        self.articles = []

        for topic in topics:

            # build our url string to make it dynamic
            full_url = URL + base + topic
            # gives us all article urls
            urls = getArticleURLs(full_url)

            for url in urls:
                new_article = Article(url, topic, article_id)

                # is it a valid article url?
                if new_article.article_id != -1:
                    article_id += 1
                    self.articles.append(new_article)
                
                # break # remove this to get all articles
        

    def write_to_JSON(self):
        filename = "articles.json"

        # we always want a fresh update so delete file each time
        if os.path.exists(filename):
            os.remove(filename)
            print(os.path.exists(filename))

        f = open("articles.json", "x")

        # do not add a comma on the last JSON entry
        size = len(self.articles)
        i = 1
        # left bracket to start JSON file
        f.write('[\n')

        for article in self.articles:
            # must be a dictionary to dump to a json
            article_json = json.dumps(article.__dict__)
            f.write(article_json)
            if i < size:
                f.write(',')

            f.write("\n")
            i += 1
        
        # close JSON content
        f.write(']')


        # we do not return anything we just write into the JSON file
        return

class Article:
    def __init__(self, url, article_type, article_id):
        try:
            title, author, full_text = RSS_Scraper(url)
            self.article_id = article_id
            self.title = title
            self.author = author
            self.url = url
            summarized = summarize(full_text)
            self.summary= summarized
            self.article_type = article_type
            print("Article {} created successfully.".format(article_id))
        except AttributeError:
            # set article_id to -1 indicating an error
            self.article_id = -1
            print("Article creation error.")


if __name__ == "__main__":
    url = "https://www.cbc.ca"
    articles = RSS_Articles(url)
    # j = json.dumps(articles.articles[0].__dict__)
    articles.write_to_JSON()
