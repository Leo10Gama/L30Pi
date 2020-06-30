import requests
from bs4 import BeautifulSoup as bs

class Move:
    def __init__(self, move_type, name, animation, details):
        self.move_type = move_type
        self.name = name
        self.animation = animation
        self.details = details

# Character dict is a dictionary linking character names to an array of moves
character_dict = {}
# Character links will link name of characters to their page
# NOTE: character names are formatted with 1) no periods 2) 'and' instead of '&' 3) all lowercase
character_links = {}
MAIN_LINK = "https://ultimateframedata.com/"
# Populate the links with characters
for character in bs(requests.get(MAIN_LINK).content, 'html.parser').find_all("div", class_="charactericon"):
    character_links[character.text.replace("\n","").lower().replace(".", "").replace("&","and")] = MAIN_LINK + character.find("a")["href"]

# Retrieve the moveset of a specific character
def get_moveset(character):
    character = character.lower().replace(".","").replace("&","and").strip()
    if character in character_dict:
        return character_dict[character]
    elif character in character_links:
        moves = bs(requests.get(MAIN_LINK + character_links[character]).content, 'html.parser')
        move_types = ["ground", "aerial", "special", "grab"]
        my_moves = []
        for i in range(0,3):
            for move in moves[i].find_all("div", class_="movecontainer"):
                move_name = ""
                move_animation = ""
                move_details = {}
                for move_info in move.children:
                    if move_info["class"] is "hitbox":
                        move_animation = MAIN_LINK + move_info.find("a")["data-featherlight"]
                    elif move_info["class"] is "movename":
                        move_name = move_info.text.replace("\n","").strip().lower()
                    else:
                        move_details[move_info["class"]] = move_info.text.replace("\n","").strip()
                my_moves.append(Move(move_types[i], move_name, move_animation, move_details))
        character_dict[character] = my_moves
        return character_dict[character]
    else:
        return "No character available"