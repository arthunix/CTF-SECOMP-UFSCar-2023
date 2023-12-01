#!/usr/bin/python

import random
import string
import sys

FLAG_LENTH = 100
FLAG_MAGIC = "SECOMPwn23{"

DEFAULT_PHRASE = "Whole Lotta Love Should be The Best Music to Listen When High"

def englishToPoorLeetspeak(message):
    """Convert the English string in message and return leetspeak."""
    # Make sure all the keys in `charMapping` are lowercase.
    """
    'a': ['4', '@', '/-\\'], 'c': ['('], 'd': ['|)'], 'e': ['3'],
    'f': ['ph'], 'h': [']-[', '|-|'], 'i': ['1', '!', '|'], 'k': [']<'],
    'o': ['0'], 's': ['$', '5'], 't': ['7', '+'], 'u': ['|_|'],
    'v': ['\\/']}
    """
    charMapping = {
        "a": ["4", "@"],
        "c": ["("],
        "d": ["|)"],
        "e": ["3"],
        "f": ["ph"],
        "i": ["1", "!"],
        "k": ["]<"],
        "o": ["0"],
        "s": ["$"],
    }
    leetspeak = ""
    for char in message:  # Check each character:
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak = leetspeak + leetReplacement
        else:
            leetspeak = leetspeak + char
    return leetspeak


def get_flag(length):
    PHRASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PHRASE
    PHRASE = PHRASE.replace(' ', '_')
    result_str = englishToPoorLeetspeak(PHRASE)

    result_flag = FLAG_MAGIC + result_str + "}"
    print(result_flag)

    return result_flag

get_flag(FLAG_LENTH)
