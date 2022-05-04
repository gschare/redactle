import requests
import json
from bs4 import BeautifulSoup, Comment

class Article:
    def __init__(self, page_name):
        self.title, self.raw_html = get_html(page_name)
        self.soup = process_html(self.title, self.raw_html)

    def to_string(self):
        return str(self.soup)

def process_html(title, raw_html):
    raw_html = '<div id="wikiframe">' + raw_html + '</div>'
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Remove the unwanted HTML elements.
    soup = strip(soup)

    # Add the title element.
    title_tag = soup.new_tag('h1')
    title_tag.string = title
    soup.div.insert(0, title_tag)

    # no need to remove Unicode--regex will match everything!
    return soup

def get_html(page_name):
    wikiurl  = 'https://en.wikipedia.org/w/api.php'
    payload = {
            'action': 'parse',
            'page': page_name,
            'format': 'json',
            'prop': 'text'
            }
    response = requests.get(wikiurl, params=payload)
    if (response.status_code != 200):
        raise Exception("could not fetch article")
    j = json.loads(response.content)
    return j['parse']['title'], j['parse']['text']['*']

def strip(soup):
    # remove disambiguation
    soup.find('div', {'class':'hatnote'}).extract()

    # remove comments
    for elt in soup(text=lambda txt: isinstance(text, Comment)):
        elt.extract()

    # remove hyperlinks but keep contents
    for elt in soup.find_all('a'):
        elt.replace_with(*elt.contents)

    # remove images
    for elt in soup.find_all('img'):
        elt.extract()

    # remove captions
    for elt in soup.find_all('div', {'class':'thumbcaption'}):
        elt.extract()

    # remove galleries
    for elt in soup.find_all('ul', {'class':'gallery'}):
        elt.extract()

    # remove tables
    for elt in soup.find_all('table'):
        elt.extract()

    # remove edit links
    for elt in soup.find_all('span', {'class':'mw-editsection'}):
        elt.extract()

    # remove reference superscripts
    for elt in soup.find_all('sup', {'class':'reference'}):
        elt.extract()

    # remove reference section
    for elt in soup.find_all('ol', {'class':'references'}):
        elt.extract()
    refs = soup.find(id='References')
    refs.extract()

    # remove table of contents
    toc = soup.find(id='toc')
    toc.extract()

    return soup

