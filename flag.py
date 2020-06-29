import requests
from bs4 import BeautifulSoup as bs
import random

class Flag:
    def __init__(self, name, flag):
        self.name = name
        self.flag = flag
    
DEFAULT = "https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags"
AMERICAN = "https://commons.wikimedia.org/wiki/Animated_GIF_flags_of_the_United_States"
flags = []
american_flags = []

# This function will return a random flag object from the preexisting list of flags
def get_random_flag(type_of_flags = ""):
    if type_of_flags == "american":
        if not american_flags:
            sections = bs(requests.get(AMERICAN).content, 'html.parser').find_all("ul", class_="gallery mw-gallery-traditional")
            for div in sections:
                for flag_list_item in div.find_all("li", class_="gallerybox"):
                    american_flags.append(Flag(flag_list_item.text.replace("\n",""), flag_list_item.find("img")["src"]))
        return american_flags[random.randrange(len(american_flags))]
    else:
        if not flags:
            sections = bs(requests.get(DEFAULT).content, 'html.parser').find_all("div", class_="mod-gallery mod-gallery-default")
            for div in sections:
                for flag_list_item in div.find_all("li", class_="gallerybox"):
                    flags.append(Flag(flag_list_item.text.replace("\n","").replace("Flag of ", ""), flag_list_item.find("img")["src"].replace("//","http://")))
        return flags[random.randrange(len(flags))]