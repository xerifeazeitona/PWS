#!/usr/bin/env python
"""
Python WS Solver (PWS)
Simple attempt to model an anagram solver for WS
"""

from collections import Counter
import sys

def create_dictionary(allow_3_letters=True):
    """Read from words.txt and create a dictionary."""
    if allow_3_letters:
        min_letters = 3
    else:
        min_letters = 4

    with open('words.txt') as file_obj:
        dic = file_obj.read()

    dic = [x.lower() for x in dic.split('\n') if len(x)>=min_letters]
    return dic

def return_anagrams(dictionary, letters: str) -> list:
    #lowercasing the input letters
    letters = letters.lower()
    letters_count = Counter(letters)

    anagrams = set()
    for word in dictionary:
        if not set(word) - set(letters):
            check_word = set()
            for k, v in Counter(word).items():
                if v <= letters_count[k]:
                    check_word.add(k)
            if check_word == set(word):
                anagrams.add(word)
    return sorted(list(anagrams), key=lambda x: len(x))

if __name__ == "__main__":
    try:
        allow_3 = str(sys.argv[2]).lower() == 'y'
    except IndexError:
        allow_3 = False

    dic = create_dictionary(allow_3)
    try:
        test_anagrams = return_anagrams(dic, sys.argv[1])
    except IndexError:
        print("Where my letters at?")
    else:
        for word in test_anagrams:
            print(word.upper())
        print(f"Number of anagrams: {len(test_anagrams)}")
