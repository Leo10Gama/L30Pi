vowels = ["a", "e", "i", "o", "u"]

def to_piglatin(phrase):
    words = phrase.split()
    returnValue = ""
    for word in words:
        returnValue += word_to_piglatin(word) + " "
    return returnValue

def word_to_piglatin(word):
    index = ""
    if word[0] in vowels:
        return word + "yay"
    for c in word:
        if c in vowels:
            index = c
            break
    else:
        return word + "yay"
    return index + word.split(index, 1)[1] + word.split(index, 1)[0] + "ay"