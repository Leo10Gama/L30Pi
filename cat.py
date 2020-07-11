import random

class Cat:
    def __init__(self, name, num_of_pics):
        self.name, self.num_of_pics = name, num_of_pics

CATS = {"ollie": Cat("ollie", 23), 
    "mushu": Cat("mushu", 8), 
    "achilles": Cat("achilles", 5), 
    "luna": Cat("luna", 8),
    "winter": Cat("winter", 6)}

# Returns an array of length 2 with the cat's name and an image of them
def get_cat_image(cat_name=""):
    # Check if a parameter has been passed
    if cat_name not in CATS:
        cat_name = random.choice(list(CATS.keys()))
    image = "cats/{}/{}.jpg".format(cat_name, random.randrange(0, CATS[cat_name].num_of_pics))
    return [cat_name.title(), image]

# Returns a list of all the cats available to see
def list_cats():
    return list(CATS.keys())