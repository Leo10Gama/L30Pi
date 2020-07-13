import requests
from bs4 import BeautifulSoup as bs

MAIN_SITE = "http://downloads.khinsider.com"

# Returns an array of dictionaries, with keys for 'title' and 'link'
def search_albums(search_term):
    search_term = search_term.replace(" ", "+")
    results = bs(requests.get(MAIN_SITE + "/search?search={}".format(search_term)).content, 'html.parser').find("div", id="EchoTopic").find_all("a")
    list_of_albums = []
    for a in results:
        list_of_albums.append({"title": a.text, "link": a["href"]})
    return list_of_albums

def get_album_by_link(link):
    album_page = bs(requests.get(link).content, 'html.parser')
    #TODO: Find a better way to format the soundtracks
    return link