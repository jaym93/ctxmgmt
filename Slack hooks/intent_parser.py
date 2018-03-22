# File: intent_parser
# Author: Jayanth M (jayanth6@gatech.edu)
# Created: 3/21/2018 10:57 PM 
# Project: ctxmgmt
# Description: Could be replaced with api.ai or wit.ai

# install adapt from pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

import json
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()

# log file for writing commands previously unheard of
logfile = open("unmatched.log", mode='a')


# text to integer conversions
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    return result + current

# register all locations in the home
locations = ["hall", "room", "nursery", "attic", "basement", "kitchen", "porch", "garage", "Backyard", "yard", "living room", "all"]
for loc in locations:
    engine.register_entity(loc, "Location")

# register all possible places
places = ["ceiling", "wall", "1", "2", "3", "floor", "door"]
# register all appliances in the home
appliances = ["light", "fan", "stove", "ac", "air conditioner", "humidifier", "dehumidifier", "door", "disc player", "heater", "microwave", "oven", "refrigerator", "washer", "dryer", "tv", "television", "computer", "light"]
# create the plurals of all appliances
appliances_plural = []
for ap in appliances:
    appliances_plural.append(ap+"s")
appliances = appliances + appliances_plural
for app in appliances:
    engine.register_entity(app, "Appliance")

# register all states which can be queried / commanded
state = ["on", "off", "open", "close", "hot", "cold", "toggle"]
for st in state:
    engine.register_entity(st, "State")

time_keywords = ["at", "in", "after", "before"]
for tk in time_keywords:
    engine.register_entity(tk, "TimeKeyword")

time_units = ["am", "pm", "hour", "hours", "minute", "minutes", "second", "seconds", "day", "days", "month", "months", "year", "years"]
for tu in time_units:
    engine.register_entity(tu, "TimeUnit")

# words that can be used to perform actions like "turn on the hallway lights"
action_keywords = ["switch", "turn", "open", "close"]
for ak in action_keywords:
    engine.register_entity(ak, "ActionKeyword")

# words that can be used to query system like "is the basement humidifier on?"
query_keywords = ["is the", "Tell me", "are the", "?"]
for qk in query_keywords:
    engine.register_entity(qk, "QueryKeyword")

# define how a query manifests
query_intent = IntentBuilder("QueryIntent") \
    .require("QueryKeyword") \
    .require("Location") \
    .require("Appliance") \
    .require("State") \
    .build()

# define how an action manifests
action_intent = IntentBuilder("ActionIntent") \
    .optionally("ActionKeyword") \
    .require("Location") \
    .require("Appliance") \
    .require("State") \
    .build()

engine.register_intent_parser(query_intent)

engine.register_intent_parser(action_intent)


def parse_intent(sentence):
    print(sentence)
    response = False
    for intent in engine.determine_intent(sentence):
        response = True
        if intent and intent.get('confidence') > 0:
            return json.dumps(intent, indent=4)
    if not response:
        logfile.write(sentence+"\n")
        logfile.flush()
        return json.dumps({"intent_type": "unknown", "confidence": 0, "message": "Sorry, I could not understand that."})

