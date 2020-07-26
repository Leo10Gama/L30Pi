import requests
from bs4 import NavigableString 
from bs4 import BeautifulSoup as bs
import re

MAIN_LINK = "https://www.ninsheetmusic.org/browse"

class Song:
    def __init__(self, title, arranger, game, sheet_id):
        self.title, self.arranger, self.game, self.sheet_id = title, arranger, game, sheet_id
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
                song.find("div", class_="tableList-cell tableList-cell--sheetArranger").get_text().replace("\n",""), 
                game.find("h3", class_="heading-text").get_text().replace("\n",""), int(song["id"][5:])))
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
        update_text = full_update_panel.find("div", class_="article-body").get_text(separator="\n").replace(new_sheets_div.get_text("\n"), "").strip('\n\t')
        # Get the actual sheets to search for
        # search_consoles is a dictionary, where console names are linked to dictionaries of games
        # where each game name is linked to an array of songs
        search_consoles = {}
        search_games = {}
        current_console = ""
        current_game = ""
        for tag in new_sheets_div.children:
            if tag.name == "em" or tag.name == "br":
                continue
            elif isinstance(tag, NavigableString):
                current_song = re.search(r'\"(.*)\"', tag.string).group()[1:-1]
                if current_game not in search_games:
                    search_games[current_game] = []
                search_games[current_game].append(current_song)
            elif tag.name == "strong":
                if current_console and current_game:
                    if current_console not in search_consoles:
                        search_consoles[current_console] = {}
                    search_consoles[current_console].update(search_games)
                current_console = re.search(r'\[(.*)\]', tag.text).group()[1:-1]
                current_game = tag.text.replace(re.search(r'\[(.*)\]', tag.text).group(), "").strip()
                search_games = {}
        # Go to each page and retrieve the sheets
        songs_to_return = []
        for console in search_consoles.keys():
            page = bs(requests.get(MAIN_LINK + "/console/{}".format(console)).content, 'html.parser')
            games = page.find_all("div", class_="contentBox contentBox--outerShadow game js-accordion isOpen")
            for game in games:
                if game.find("h3").text.strip().replace("\n", "") in search_consoles[console].keys():
                    for song_li in game.find_all("li"):
                        if song_li.find("div", class_="tableList-cell tableList-cell--sheetTitle").text.strip().replace("\n","") in search_consoles[console][game.find('h3').text.strip().replace("\n","")]:
                            songs_to_return.append(Song(song_li.find("div", class_="tableList-cell tableList-cell--sheetTitle").get_text().replace("\n",""),
                                song_li.find("div", class_="tableList-cell tableList-cell--sheetArranger").get_text().replace("\n",""), 
                                game.find('h3').text.strip().replace("\n",""), int(song_li["id"][5:])))
    else:
        update_text = full_update_panel.find("div", class_="article-body").get_text(separator="\n").strip('\n\t')
    return {"title": update_title, "text": update_text, "songs": songs_to_return}
    