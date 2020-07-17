import requests
from bs4 import BeautifulSoup as bs

MAIN_LINK = "https://www.ninsheetmusic.org/browse"

class Song:
    def __init__(self, title, arranger, sheet_id):
        self.title, self.arranger, self.sheet_id = title, arranger, sheet_id
        save_types = ["pdf", "mid", "mus"]
        self.links = {}
        for save_type in save_types:
            self.links[save_type] = "https://www.ninsheetmusic.org/download/{}/{}".format(save_type, str(sheet_id))


# Compile the list of available game series or consoles in a dictionary with the respective link
def get_list(type_of_list="series"):
    lists = bs(requests.get(MAIN_LINK + "/{}".format(type_of_list)).content, 'html.parser').find_all("ul", class_="browseCategoryList-subList")
    return_value = {}
    for ul_tag in lists:
        for list_item in ul_tag.find_all("li"):
            return_value[list_item.get_text().lower().replace("é","e")] = list_item.find("a")["href"]
    return return_value

# Returns a dictionary object, where each entry contains an array of other dictionaries
# These 'subdictionaries' contain song title, arranger, and a download link to a pdf of the sheet music
def get_sheets_from_page(link):
    sheets = {}
    games = bs(requests.get(link).content, 'html.parser').find_all("div", class_="game")
    for game in games:
        songs = []
        for song in game.find_all("li"):
            songs.append(Song(song.find("div", class_="tableList-cell tableList-cell--sheetTitle").get_text().replace("\n",""),
                song.find("div", class_="tableList-cell tableList-cell--sheetArranger").get_text().replace("\n",""), int(song["id"][5:])))
        else:
            sheets[game.find("h3", class_="heading-text").get_text().replace("\n","").replace("é","e")] = songs
    else:
        return sheets