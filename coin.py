import requests
from bs4 import BeautifulSoup as bs

MAIN_SITE = "http://en.numista.com"
SEARCH_SITE = "http://en.numista.com/catalogue/index.php?mode=avance"
# The site Numista uses alternate country names (mostly french) to search, so we must encode a quick replacement
country_dictionary = {
    "canada": "canada_section",
    "united states": "united-states",
    "us": "united-states",
    "usa": "united-states",
    "algeria": "algerie",
    "armenia": "armenie",
    "australia": "australia_section",
    "the bahamas": "bahamas",
    "bahrain": "bahrein",
    "barbados": "barbade",
    "belarus": "bielorussie",
    "belize": "belize_section",
    "bermuda": "bermudes",
    "bolivia": "bolivie",
    "bosnia and herzegovina": "bosnia_herzegovina_section",
    "bosnia & herzegovina": "bosnia_herzegovina_section",
    "brazil": "brazil_section",
    "bulgaria": "bulgaria_section",
    "cameroon": "cameroon_section",
    "cayman islands": "iles_caimanes",
    "cayman isles": "iles_caimanes",
    "chile": "chili",
    "colombia": "colombie",
    "cook islands": "iles_cook",
    "cook isles": "iles_cook",
    "costa rica": "costa_rica",
    "cyprus": "chypre",
    "czech republic": "czech",
    "czechoslovakia": "tchecoslovaquie",
    "ecuador": "equateur",
    "egypt": "egypte",
    "estonia": "estonia_section",
    "fiji": "fidji",
    "finland": "finlande",
    "france": "france_section",
    "georgia": "georgia_section",
    "ghana": "ghana_section",
    "iceland": "islande",
    "iraq": "irak",
    "ireland": "irlande",
    "isle of man": "ile_de_man",
    "israel": "israel_section",
    "jamaica": "jamaique",
    "japan": "japon",
    "malta": "malte",
    "new zealand": "nouvelle_zelande",
    "nigeria": "nigeria_section",
    "north korea": "coree_du_nord",
    "north macedonia": "macedoine",
    "oman": "oman_section",
    "papua new guinea": "papua-new-guinea",
    "peru": "perou",
    "poland": "poland_section",
    "portugal": "portugal_section",
    "romania": "roumanie",
    "san marino": "saint-marin",
    "saudi arabia": "saudi-arabia",
    "serbia": "serbia_section",
    "slovakia": "slovaquie",
    "slovenia": "slovenie",
    "south africa": "south-africa",
    "south korea": "coree_du_sud",
    "sri lanka": "sri-lanka",
    "sweden": "sweden_section",
    "syria": "syrie",
    "thailand": "thailande",
    "trinidad and tobago": "trinite-et-tobago_section",
    "trinidad": "trinite-et-tobago_section",
    "trinidad & tobago": "trinite-et-tobago_section",
    "turkey": "turquie",
    "united arab emirates": "uae",
    "united kingdom": "united-kingdom",
    "uk": "united-kingdom",
    "vatican city": "vatican",
    "venezuela": "venezuela_section",
    "vietnam": "viet-nam",
    "yemen": "yemen_section",
    "yugoslavia": "yougoslavie",
    "zimbabwe": "zimbabwe_section",
}

class Coin:
    def __init__(self, name, obverse, reverse, properties, link):
        self.name, self.obverse, self.reverse, self.properties, self.link = name, obverse, reverse, properties, link


def map_country(country):
    for key in country_dictionary.keys():
        if country == key:
            return country_dictionary[country]
    else:
        return country.lower()

def get_coins(country="", year="", face_value="", query=""):
    year, face_value, query = map(lambda x: x.strip().replace(" ", "+"), (year, face_value, query))
    site_link = SEARCH_SITE + "&e={}".format(map_country(country)) + "&d={}".format(query) + "&v={}".format(face_value) + "&a={}".format(year)
    page = bs(requests.get(site_link).content, 'html.parser')
    results = page.find_all("div", class_="resultat_recherche")
    if len(results) == 0:
        return False
    elif len(results) == 1:
        return get_coin_by_link(MAIN_SITE + results[0].find("a")["href"])
    else:
        list_of_coins = []
        for result in results:
            list_of_coins.append({"name": ' '.join(result.find("div", class_="description_piece").find("a").text.replace("\n","").split()),
                "link": MAIN_SITE + result.find("a")["href"]})
        return list_of_coins

def get_coin_by_link(link):
    page = bs(requests.get(link).content, 'html.parser')
    coin_name = page.find("h1").text.replace("\n","")
    coin_obv, coin_rev = map(lambda img: img["src"], page.find("div", id="fiche_photo").find_all("img"))
    coin_properties = {}
    for tr in page.find("section", id="fiche_caracteristiques").find("table").find_all("tr"):
        if not tr.find("th").text == "References":
            coin_properties[tr.find("th").text] = ' '.join(tr.find("td").text.replace("\n","").replace("&nbsp"," ").split())
    return Coin(coin_name, coin_obv, coin_rev, coin_properties, link)