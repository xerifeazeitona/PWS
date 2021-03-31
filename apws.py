#!/usr/bin/env python
"""
Python WS Solver (PWS) - Automated edition
Simple attempt to model an anagram solver for WS
This version has access to a database of letters for each level, so all
you have to input is the desired level and it will return the words.
The only downside is that there is no way to inform if 3 letter words
should be omitted but the speed gains are more than worth it.
"""

from collections import Counter
import sys
import shelve

FILENAME = 'curated_words.txt'

def create_dictionary(allow_3_letters=True):
    """Read from FILENAME and create a dictionary."""
    if allow_3_letters:
        min_letters = 3
    else:
        min_letters = 4

    with open(FILENAME) as file_obj:
        dic = file_obj.read()

    dic = [x.lower() for x in dic.split('\n') if len(x)>=min_letters]
    return dic

def return_anagrams(dictionary, letters: str) -> list:
    """
    Returns a list of 'dictionary' words that can be created with the
    'letters' provided
    """
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

def read_level_data():
    """Read level data from shelve file"""
    data_dic = {}
    shelf_file = shelve.open('level_data')
    for key, value in shelf_file.items():
        data_dic[key] = value
    shelf_file.close()
    return dict(sorted(data_dic.items(), key=lambda item: int(item[0])))

def validate_input():
    """Only valid argument is the level and it has to be in the master range"""
    try:
        input_level = int(sys.argv[1])
    except IndexError:
        print('apws: missing level argument')
        print("Try './apws LEVEL' next time.")
        sys.exit()
    except ValueError:
        print('apws: invalid level argument')
        print("Try './apws LEVEL' where LEVEL is a number next time.")
        sys.exit()
    if input_level <= 6000:
        print('This program only works with MASTER levels (6001 and above).')
        sys.exit()
    return input_level

if __name__ == "__main__":
    # Basic validation
    level = validate_input()

    # Create letters dictionary
    letters_dic = read_level_data()

    # Create words dictionary
    words_dic = create_dictionary()

    while True:
        # Get valid words for the level
        test_anagrams = return_anagrams(words_dic, letters_dic[str(level)])

        # display valid words + total
        print(f'\nFound {len(test_anagrams)} words for level {level}:')
        for valid_word in test_anagrams:
            print(valid_word.upper())

        # prompts for next level
        if input('\nProceed to next level? [Y/n] ').lower() == 'n':
            sys.exit()
        level += 1
