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

# Returns a dictionary object, where each entry contains an array of song objects
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

# Returns the most recent NSM update information, including title, text, and new sheets
def get_update():
    full_update_panel = bs(requests.get("https://www.ninsheetmusic.org").content, 'html.parser').find("article")
    update_title = full_update_panel.find("h3").text
    new_sheets_div = full_update_panel.find("div", attrs={"align": "center"})
    if bool(new_sheets_div):
        # TODO: List and get the actual sheets
        update_text = full_update_panel.find("div", class_="article-body").get_text(separator="\n").replace(new_sheets_div.get_text("\n"), "").strip('\n\t')
    else:
        update_text = full_update_panel.find("div", class_="article-body").get_text(separator="\n").strip('\n\t')
    return {"title": update_title, "text": update_text}
    