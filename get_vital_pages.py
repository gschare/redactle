import requests
from bs4 import BeautifulSoup, Tag

url = "https://meta.wikimedia.org/wiki/List_of_articles_every_Wikipedia_should_have/Expanded"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

for listitem in soup.find_all('li'):
    link = listitem.find('a', {'class':'extiw'})
    if link:
        print(link.string)
