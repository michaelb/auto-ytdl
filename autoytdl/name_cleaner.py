#!/bin/python3

import sys
import os
import re

from mp3_tagger import MP3File, VERSION_2
"""to clean trash from a .mp3 tags"""


def remove_brackets(string):
    string = re.sub(r'\(\)', '', string)
    string = re.sub(r'\( \)', '', string)
    string = re.sub(r'\(  \)', '', string)
    # dont want to test more compelx regex for this
    string = re.sub(r'\(   \)', '', string)
    string = re.sub("[\{\[].*?[\}\]]", "", string)
    return string


def remove_denylisted_names(string, config):
    expanded_denylist = config.denylist_names
    expanded_denylist = [x+"s" for x in expanded_denylist] + expanded_denylist
    expanded_denylist = expanded_denylist + \
        [x.lower() for x in expanded_denylist] + [x.upper()
                                                  for x in expanded_denylist]
    for banned_name in expanded_denylist:
        string = string.replace(banned_name, '')
    return string


def cleanstr(string, config):
    string = string.strip()  # remove trailing and leading whitespaces
    string = remove_denylisted_names(string, config)
    string = remove_brackets(string)
    return string


def fix_duration(filepath):
    # Create a temporary name for the current file.
    # i.e: 'sound.mp3' -> 'sound_temp.mp3'
    temp_filepath = filepath[:len(filepath) - len('.mp3')] + '_temp' + '.mp3'

    # Rename the file to the temporary name.
    os.rename(filepath, temp_filepath)

    # Run the ffmpeg command to copy this file.
    # This fixes the duration and creates a new file with the original name.
    command = 'ffmpeg -v quiet -i "' + temp_filepath + \
        '" -acodec copy "' + filepath + '"'
    os.system(command)

    # Remove the temporary file that had the wrong duration in its metadata.
    os.remove(temp_filepath)


def clean(filepath, config):
    mp3 = MP3File(filepath)
    mp3.set_version(VERSION_2)
    title = mp3.song
    artist = mp3.artist

    mp3.song = cleanstr(title, config)
    mp3.artist = cleanstr(artist, config)

    mp3.save()
    fix_duration(filepath)
