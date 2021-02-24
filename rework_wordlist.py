#!/usr/bin/env python
"""
This simple module removes all the words that have less than 2 or more
than 7 characters, since they can't be used in the game.
"""

input_file = 'words.txt'
output_file = 'valid_words.txt'

with open(input_file) as file_obj:
    words = file_obj.read()

words = [x.lower() for x in words.split('\n') if len(x)>=3 and len(x)<=7]

with open(output_file, 'w') as file_obj:
    for word in words:
        file_obj.write(f"{word}\n")
