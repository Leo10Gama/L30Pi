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
    if character.find("span"):
        character_links[character.text.replace(character.find("span").get_text(), "").replace("\n","").lower().replace(".", "").replace("&","and")] = MAIN_LINK + character.find("a")["href"]
    else:
        character_links[character.text.replace("\n","").lower().replace(".", "").replace("&","and")] = MAIN_LINK + character.find("a")["href"]

move_info_formatting = {
    "totalframes": "Total Frames",
    "landinglag": "Landing Lag",
    "basedamage": "Base Damage",
    "shieldlag": "Shield Lag",
    "shieldstun": "Shield Stun",
    "whichhitbox": "Which Hitbox",
    "activeframes": "Active Frames"
}

# Retrieve the moveset of a specific character
# Returns an array of moves matching the character
def get_moveset(character):
    character = character.lower().replace(".","").replace("&","and").strip()
    if character in character_dict:
        return character_dict[character]
    elif character in character_links:
        moves = bs(requests.get(character_links[character]).content, 'html.parser').find("div", id="contentcontainer").find_all("div", class_="moves")
        move_types = ["ground", "aerial", "special", "grab"]
        my_moves = []
        for i in range(0,4):
            for move in moves[i].find_all("div", class_="movecontainer"):
                move_name = ""
                move_animation = []
                move_details = {}
                for move_info in move.find_all("div"):
                    if move_info["class"][0] == "hitbox":
                        # Move has multiple hitboxes
                        if len(move_info.find_all("a")) > 1:
                            move_animation = []
                            for item in move_info.find_all("a"):
                                move_animation.append(MAIN_LINK + item["data-featherlight"])
                        # Only one hitbox
                        else:
                            try:
                                move_animation.append(MAIN_LINK + move_info.find("a")["data-featherlight"])
                            except:
                                pass
                    elif move_info["class"][0] == "movename":
                        move_name = move_info.text.replace("\n","").strip().lower()
                    else:
                        if move_info.text.replace("\n","").strip() != "--":
                            if move_info["class"][0] in move_info_formatting:
                                move_details[move_info_formatting[move_info["class"][0]]] = move_info.text.replace("\n","").strip()
                            else:
                                move_details[move_info["class"][0].title()] = move_info.text.replace("\n","").strip()
                my_moves.append(Move(move_types[i], move_name, move_animation, move_details))
        character_dict[character] = my_moves
        return character_dict[character]
    else:
        return "No character available"