import regex
from bs4 import BeautifulSoup, NavigableString

class Page:
    def __init__(self, soup, dictionary):
        self.soup, self.words = tag_words(make_page(soup), dictionary)

    def update(self, word):
        self.update_guesses(word)
        self.update_wikipage(word)

    def update_guesses(self, word):
        pass

    def update_wikipage(self, word):
        pass

    def highlight(self):
        pass

    def __repr__(self):
        return str(self.soup)

def tag_words(soup, dictionary):
    # tag every word with span and a class saying it's a word
    # each one has an attribute saying which word it is, this is for easy
    # updating simply by changing the relevant CSS rule.
    # also a tag for whether it's in the dictionary.
    # keep a log of each one
    # i have no idea if this will work
    words_ = {}
    # also make all the words in the dict lower

    for elt in soup.find(id='wikiframe').descendants:
        if isinstance(elt, NavigableString):
            parts = regex.findall(r"[\w']+|[^\w\s]", str(elt), regex.UNICODE)
            for word in parts:
                word_tag = soup.new_tag('span')
                word_tag['class'] = f'word word-{word}' + (' default-word' if word in dictionary else '')
                word_tag.string = word
                words
            #elt.replace_with(
    return soup, words_

def make_page(soup):
    # Reframe the HTML content into a page with a scrolling box, a list of
    # guesses, and an input form.

    soup.div['style'] = """
    width: 70%;
    height: 90%;
    overflow: scroll;
    display: inline-block;
    """

    guesses_div = soup.new_tag('div')
    guesses_div['id'] = 'guesses'
    guesses_div.append(make_guesses(soup))
    guesses_div['style'] = """
    width: 25%;
    height: 90%;
    overflow: scroll;
    display: inline-block;
    """

    input_div = soup.new_tag('div')
    input_div['id'] = 'input'
    input_div.append(make_form(soup))
    input_div['style'] = """
    align: center;
    height: 10%;
    """

    main_div = soup.new_tag('div')
    main_div['id'] = 'main'

    main = soup.div.wrap(main_div)
    main.append(guesses_div)
    main.append(input_div)

    return main.wrap(soup.new_tag('html'))

def make_form(soup):
    form = soup.new_tag('form')
    form['method'] = 'POST'
    input_box = soup.new_tag('input')
    input_box['name'] = 'guess'
    submit = soup.new_tag('input')
    submit['type'] = 'submit'
    submit['style'] = 'display: none'
    form.append(input_box)
    form.append(submit)
    return form

def make_guesses(soup):
    return ""
