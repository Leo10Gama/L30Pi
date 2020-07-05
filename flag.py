import requests
from bs4 import BeautifulSoup as bs
import random
import re

class Flag:
    def __init__(self, name, image):
        self.name = name
        self.image = image
    
DEFAULT = "https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags"
AMERICAN = "https://commons.wikimedia.org/wiki/Animated_GIF_flags_of_the_United_States"
ARMS = "https://en.wikipedia.org/wiki/Armorial_of_sovereign_states"
CANADIAN = "https://en.wikipedia.org/wiki/List_of_Canadian_flags"
flags = []
american_flags = []
arms = []
canadian_flags = []

# This function will return a random flag object from the preexisting list of flags
def get_flags(type_of_flags = ""):
    if type_of_flags == "america":
        if not american_flags:
            sections = bs(requests.get(AMERICAN).content, 'html.parser').find_all("ul", class_="gallery mw-gallery-traditional")
            for div in sections:
                for flag_list_item in div.find_all("li", class_="gallerybox"):
                    american_flags.append(Flag(flag_list_item.text.replace("\n",""), flag_list_item.find("img")["src"]))
        return american_flags
    elif type_of_flags == "arms":
        if not arms:
            sections = bs(requests.get(ARMS).content, 'html.parser').find_all("ul", class_="gallery mw-gallery-traditional")
            for div in sections:
                for arm_list_item in div.find_all("li", class_="gallerybox"):
                    arms_name = arm_list_item.text.replace("\n","")
                    arms_name = re.split(r'of', arms_name)[len(re.split(r'of', arms_name)) - 1]
                    arms_name = re.sub(r'\([^)]*\)', "", re.sub(r'\[[^]]*\]', "", re.sub(r',[a-zA-Z0-9\s]*', '', arms_name))).strip()
                    arms.append(Flag(arms_name, arm_list_item.find("img")['src']))
        return arms
    elif type_of_flags == "canada":
        if not canadian_flags:
            tables = bs(requests.get(CANADIAN).content, 'html.parser').find_all("table", class_="wikitable")
            sections = tables[6].find_all("tr")[1:] + tables[7].find_all("tr")[1:]
            for row in sections:
                tds = row.find_all("td")
                canadian_flags.append(Flag(re.sub(r'\([^)]*\)', "", tds[2].text.replace("\n","").replace("Flag of ","").strip()), "http:" + tds[0].find("img")["src"]))
        return canadian_flags
    else:
        if not flags:
            sections = bs(requests.get(DEFAULT).content, 'html.parser').find_all("div", class_="mod-gallery mod-gallery-default")
            for div in sections:
                for flag_list_item in div.find_all("li", class_="gallerybox"):
                    flags.append(Flag(flag_list_item.text.replace("\n","").replace("Flag of ", ""), "http:" + flag_list_item.find("img")["src"]))
        return flags