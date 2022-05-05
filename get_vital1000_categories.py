import requests
from bs4 import BeautifulSoup, Tag

url = "https://meta.wikimedia.org/wiki/List_of_articles_every_Wikipedia_should_have/Expanded"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

for category in [t for t in soup.find(id='toc').ul.contents if isinstance(t, Tag)]:
    cat = category.contents[0].contents[-1].string.split(', ')
    catname = cat[0]
    catnum = cat[1]
    catid = category.contents[0]['href']
    cats[catid] = {}
    print(catid, catname)
    for subcategory in [t for t in category.ul.contents if isinstance(t, Tag)]:
        subcat = subcategory.contents[0].contents[-1].string.split(', ')
        subcatname = subcat[0]
        subcatnum = subcat[1]
        subcatid = subcategory.contents[0]['href']
        cats[catid][subcatid] = []
        print(subcatid, subcatname)

