import sys
import requests
import random
import regex
from bs4 import BeautifulSoup

from article import Article
from page import Page

DEFAULT_DICTIONARY = "defaultwords.txt"
DEFAULT_ARTICLES = "articles.txt"

def load_article_names(filepath):
    articles = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            articles.append(line.rstrip())
    return articles

def load_dictionary(filepath):
    dictionary = set()
    with open(filepath, 'r') as f:
        for line in f.readlines():
            dictionary.add(line.rstrip())
    return dictionary

class Game:
    def __init__(self, page=None, seed=None):
        self.dictionary = load_dictionary(DEFAULT_DICTIONARY)
        self.guessed = {}
        self.unguessed = None
        self.answer = None
        if page:
            self.set_article(page)
        else:
            self.random_article(seed=seed)

    def set_article(self, page):
        self.article = Article(page)
        self.page = Page(self.article.soup, self.dictionary)
        self.answer = { k.lower():False for k in self.article.title.split(' ') }
        print(self.article.title, file=sys.stderr, flush=True)
        self.unguessed = { k:v for k,v in self.page.words.items() }

    def random_article(self, seed=None):
        articles = load_article_names(DEFAULT_ARTICLES)
        if seed is not None:
            article = articles[seed % len(articles)]
        else:
            article = articles[random.randrange(len(articles))]
        #response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        self.set_article(article)

    def guess(self, word):
        word = word.lower()
        # TODO: normalize guess
        print(word, file=sys.stderr, flush=True)
        if regex.match(r'.*[\s].*', word):
            return

        if word in self.dictionary:
            self.highlight(word)
            return

        if self.guessed.get(word) is not None:
            self.highlight(word)
            return

        # if regex matches a word in unguessed
        if self.unguessed.get(word) is not None:
            # then remove it from unguessed, add it to guessed
            self.guessed[word] = self.unguessed[word]
            del self.unguessed[word]

            if word in self.answer:
                self.answer[word] = True
            if all([v for k,v in self.answer.items()]):
                self.highlight(word)
                self.page.update(word)
                self.win()
                return
            # update the page
            self.highlight(word)
            self.page.update(word)
        else:
            self.page.make_guess(word)
        self.page.update_wikipage()

    def highlight(self, word):
        self.page.highlight(word)

    def display(self):
        return str(self.page)

    def win(self):
        self.page.win()
