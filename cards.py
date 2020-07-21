import random

DECK = []
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]     # In order from left to right: spade, heart, diamond, club
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
for value in VALUES:
    for suit in SUITS:
        DECK.append(value + suit)

# Return a shuffled deck of cards (string of value, followed by ascii of suit)
def get_shuffled_deck():
    temp = DECK
    random.shuffle(temp)
    return temp