import flag
import random

# The item being returned should always be an object with properties 'name' and 'image'
def get_question(question_type):
    collection = []
    if question_type == "flag":
        collection = flag.get_flags()
    elif question_type == "flag america":
        collection = flag.get_flags("american")
    elif question_type == "flag arms":
        collection = flag.get_flags("arms")
    return_item = collection[random.randrange(len(collection))]
    return return_item