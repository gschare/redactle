import regex
import sys
from bs4 import BeautifulSoup, NavigableString

class Page:
    def __init__(self, soup, dictionary):
        self.n_guesses = 0
        self.soup = make_page(soup)
        self.soup, self.words = tag_words(self.soup, dictionary)

        self.styles = self.style(list(self.words.keys()))
        self.update_wikipage()

    def update(self, guess):
        self.make_guess(guess)
        self.uncover_word(guess)
        self.update_wikipage()

    def win(self):
        for word in self.words.keys():
            self.uncover_word(word)
        self.update_wikipage()

    def uncover_word(self, word):
        self.styles['words'][word] = """
            span.word-"""+word+""" {
                background-color: transparent;
                color: a3a3a3;
            }
            """

    def make_guess(self, guess):
        self.n_guesses += 1
        guess_col = self.soup.find('div', id='guesses').find('ul')
        new_guess = self.soup.new_tag('li')
        hits = self.words.get(guess) or 0
        print(guess, self.words.get(guess), file=sys.stderr, flush=True)
        new_guess.string = '#' + str(self.n_guesses) + ' | ' + guess + ' - ' + str(hits)
        guess_col.insert(0, new_guess)

    def update_wikipage(self):
        defaults = "\n".join(self.styles['default'])
        highlights = "\n".join(self.styles['highlights'].values())
        words = "\n".join(self.styles['words'].values())
        self.soup.head.style.string = defaults + '\n' + words + '\n' + highlights

    def highlight(self, word):
        self.styles['highlights'] = {}
        self.styles['highlights'][word] = """
            span.word-"""+word+""" {
                background-color: rgba(255, 200, 100, 0.9);
                color: black;
            }"""

    def style(self, words):
        styles = { "default": [],
                   "highlights": {},
                   "words": {} }
        styles['default'].append("""
            html {
                background-color: #232323;
                color: #a3a3a3;
            }
            body {
                font-family: monospace;
                font-size: 16;
                line-height: 150%;
            }
            span {
                background-color: transparent;
                color: #a3a3a3;
            }
            span.nonword {
                background-color: transparent;
                color: #a3a3a3;
            }
            span.default-word {
                background-color: transparent;
                color: #a3a3a3;
            }
            """)

        for word in words:
            styles['words'][word] = """
            span.word-"""+word+""" {
                background-color: #989898;
                color: transparent;
            }
            """
        return styles

    def __repr__(self):
        return str(self.soup)

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
                    # TODO: normalize the word
                    if word_lower in words:
                        words[word_lower] += 1
                    elif word_lower not in dictionary:
                        words[word_lower] = 1
                    word_tag = soup.new_tag('span')
                    word_tag['class'] = f'word word-{word_lower}' + (' default-word' if word_lower in dictionary else '')
                    word_tag.string = word
                    tag.append(word_tag)
                else:
                    word_tag = soup.new_tag('span')
                    word_tag['class'] = 'nonword'
                    word_tag.string = s[match.start():match.end()]
                    tag.append(word_tag)
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
    lst = soup.new_tag('ul')
    return lst

