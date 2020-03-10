from RSSfeed import getArticleURLs
from scraper import RSS_Scraper
import nltk
import heapq

"""
    Returns a list of articles from an RSS feed

    Each entry is an Article object

    Todo:
        -remove blocks for all articles, it currently looks at only one
"""


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

        for url in urls:
            new_article = Article(url)
            self.articles.append(new_article)
            break # remove this for all articles

class Article:
    def __init__(self, url):
        title, author, full_text = RSS_Scraper(url)
        self.title = title
        self.author = author
        summarized = summarize(full_text)
        self.summary= summarized



if __name__ == "__main__":
    url = "https://www.cbc.ca/cmlink/rss-politics"
    articles = RSS_Articles(url)
    print(articles.articles[0].summary)
