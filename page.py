import regex
import sys
from bs4 import BeautifulSoup, NavigableString

class Page:
    def __init__(self, soup, dictionary):
        self.soup = make_page(soup)
        self.soup, self.words = tag_words(self.soup, dictionary)

        self.soup = style(self.soup, [], list(self.words.keys()))

    def update(self, guessed, unguessed):
        self.update_guesses(guessed)
        self.update_wikipage(guessed, unguessed)

    def update_guesses(self, word):
        pass

    def update_wikipage(self, guessed, unguessed):
        self.soup = style(self.soup, guessed, unguessed)

    def highlight(self, word):
        #self.soup.head.style
        pass

    def __repr__(self):
        return self.soup.prettify()

def tag_words(soup, dictionary):
    # tag every word with span and a class saying it's a word
    # each one has an attribute saying which word it is, this is for easy
    # updating simply by changing the relevant CSS rule.
    # also a tag for whether it's in the dictionary.
    # keep a log of each one
    words = {}

    for elt in list(soup.html.find('div', id='wikiframe').descendants):
        if isinstance(elt, NavigableString):
            s = str(elt)
            matches = regex.finditer(r"([\w'])+|[^\w]", s, regex.UNICODE)
            tag = soup.new_tag("span")
            for match in matches:
                if match.group(1) is not None:
                    word = s[match.start():match.end()]
                    word_lower = word.lower()
                    if word_lower in words:
                        words[word_lower] += 1
                    else:
                        words[word_lower] = 1
                    word_tag = soup.new_tag('span')
                    word_tag['class'] = f'word word-{word_lower}' + (' default-word' if word_lower in dictionary else '')
                    word_tag.string = word
                    tag.append(word_tag)
                else:
                    tag.append(s[match.start():match.end()])
            elt.replace_with(tag)

    return soup, words

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
    main.wrap(soup.new_tag('html'))

    return soup

def make_form(soup):
    form = soup.new_tag('form')
    form['method'] = 'POST'
    input_box = soup.new_tag('input')
    input_box['name'] = 'guess'
    input_box['autofocus'] = 'true'
    submit = soup.new_tag('input')
    submit['type'] = 'submit'
    submit['style'] = 'display: none'
    form.append(input_box)
    form.append(submit)
    return form

def make_guesses(soup):
    return ""

def style(soup, guessed, unguessed):
    styles = []
    for word in unguessed:
        styles.append("""
        span.word-"""+word+""" {
            background-color: black;
            color: transparent;
        }
        """)
    for word in guessed:
        styles.append("""
        span.word-"""+word+""" {
            background-color: transparent;
            color: black;
        }
        """)
    styles.append("""
        span.default-word {
            background-color: transparent;
            color: black;
        }
        """)
    soup.head.style.string = "\n".join(styles)
    return soup
