import requests
from bs4 import BeautifulSoup as bs

MAIN_LINK = "https://www.ninsheetmusic.org/browse"

# Compile the list of available game series in a dictionary with the respective link
def get_series_list():
    lists = bs(requests.get(MAIN_LINK + "/series").content, 'html.parser').find_all("ul", class_="browseCategoryList-subList")
    return_value = {}
    for ul_tag in lists:
        for list_item in ul_tag.find_all("li"):
            return_value[list_item.get_text().lower()] = list_item.find("a")["href"]
    return return_value

# Compile the list of available consoles in a dictionary with the respective link
def get_console_list():
    lists = bs(requests.get(MAIN_LINK + "/console").content, 'html.parser').find_all("ul", class_="browseCategoryList-subList")
    return_value = {}
    for ul_tag in lists:
        for list_item in ul_tag.find_all("li"):
            return_value[list_item.get_text().lower()] = list_item.find("a")["href"]
    return return_value

# Returns a dictionary object, where each entry contains an array of other dictionaries
# These 'subdictionaries' contain song title, arranger, and a download link to a pdf of the sheet music
def get_sheets_from_page(link):
    SHEET_DOWNLOAD_LINK = "https://www.ninsheetmusic.org/download/pdf/"
    sheets = {}
    games = bs(requests.get(link).content, 'html.parser').find_all("div", class_="game")
    for game in games:
        songs = []
        for song in game.find_all("li"):
            songs.append({
                "title": song.find("div", class_="tableList-cell tableList-cell--sheetTitle").get_text().replace("\n",""), 
                "arranger": song.find("div", class_="tableList-cell tableList-cell--sheetArranger").get_text().replace("\n",""),
                "link": SHEET_DOWNLOAD_LINK + song["id"][5:]})
        else:
            sheets[game.find("h3", class_="heading-text").get_text().replace("\n","")] = songs
    else:
        return sheets