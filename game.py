from bs4 import BeautifulSoup
import regex
from article import Article
from page import Page
import sys
import requests

DEFAULT_DICTIONARY = "defaultwords.txt"

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
        self.unguessed = self.page.words

    def random_article(self, seed=None):
        response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        self.set_article(response.url.split('/')[-1])

    def guess(self, word):
        word = word.lower()
        print(word, file=sys.stderr, flush=True)
        if regex.match(r'.*[\s].*', word):
            return
        #query = regex.compile(ur'(?fi)\L<opts>', opts=[word])

        if word in self.dictionary:
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
                self.win()
                return
            # update the page
            self.page.update(list(self.guessed.keys()), list(self.unguessed.keys()))
            self.highlight(word)

    def highlight(self, word):
        self.page.highlight(word)

    def display(self):
        return str(self.page)

    def win(self):
        self.guessed.update(self.unguessed)
        self.unguessed = {}
        self.page.update(list(self.guessed.keys()), list(self.unguessed.keys()))
