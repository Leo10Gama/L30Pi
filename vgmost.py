import requests
from bs4 import BeautifulSoup as bs

class Song:
    def __init__(self, title, track_number, link, disk_number=1):
        self.title, self.track_number, self.disk_number, self.link = title, track_number, disk_number, link

class Album:
    def __init__(self, title, art, songlist, link):
        self.title, self.art, self.songlist, self.link = title, art, songlist, link

MAIN_SITE = "http://downloads.khinsider.com"

# Returns an array of dictionaries, with keys for 'title' and 'link'
def search_albums(search_term):
    search_term = search_term.replace(" ", "+")
    search_link = MAIN_SITE + "/search?search={}".format(search_term)
    page = bs(requests.get(search_link).content, 'html.parser').find("div", id="EchoTopic")
    results = page.find_all("a")
    list_of_albums = []
    if page.find("table", id="songlist"):
        list_of_albums.append({"title": page.find("h2").text, "link": search_link})
        return list_of_albums
    else:
        for a in results:
            list_of_albums.append({"title": a.text, "link": a["href"]})
        return list_of_albums

# Returns an Album object
def get_album_by_link(link):
    album_page = bs(requests.get(link).content, 'html.parser').find("div", id="EchoTopic")
    album_title = album_page.find("h2").text
    album_art = album_page.find("table").find("img")
    if not album_art: album_art = ""
    else: album_art = album_art["src"]
    main_table = album_page.find("table", id="songlist")
    disk_i, track_i, song_i = "", "", ""
    i = 0
    # Figure out the index of the table rows
    for th in main_table.find("tr", id="songlist_header").find_all("th"):
        if th.text.strip().replace("\n","") == "CD":
            disk_i = i
        elif th.text.strip().replace("\n","") == "#":
            track_i = i
        elif th.text.strip().replace("\n","") == "Song Name":
            song_i = i
        i += 1
    if not disk_i: disk_i=-1
    if not track_i: track_i=-1
    songlist = []
    # Actually get the information
    for tr in main_table.find_all("tr"):
        if tr.get("id") == "songlist_header" or tr.get("id") == "songlist_footer": continue
        tds = tr.find_all("td")
        song_title = tds[song_i].text
        link = MAIN_SITE + tds[song_i].find("a")["href"]
        if track_i != -1: track_number = tds[track_i].text
        else: track_number = "?"
        if disk_i != -1: disk_number = tds[disk_i].text
        else: disk_number = 1
        if len(songlist) < int(disk_number): songlist.append([])
        songlist[int(disk_number) - 1].append(Song(song_title, track_number, link, disk_number))
    return Album(album_title, album_art, songlist, link)