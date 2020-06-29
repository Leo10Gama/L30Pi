import requests
from bs4 import BeautifulSoup as bs
import random

class Flag:
    def __init__(self, name, flag):
        self.name = name
        self.flag = flag
    
LINK = "https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags"
flags = []

# This function will return a random flag object from the preexisting list of flags
def get_random_flag():
    # Only execute this once to save time
    if not flags:
        sections = bs(requests.get(LINK).content, 'html.parser').find_all("div", class_="mod-gallery mod-gallery-default")
        for div in sections:
            for flag_list_item in div.find_all("li", class_="gallerybox"):
                flags.append(Flag(flag_list_item.text.replace("\n","").replace("Flag of ", ""), flag_list_item.find("img")["src"].replace("//","http://")))
    return flags[random.randrange(len(flags))]