#!/bin/python3

import sys
import os
import re
from pathlib import Path

import music_tag
"""to clean trash from a audio file tags"""


def remove_brackets(string):
    string = re.sub(r'\(\)', '', string)
    string = re.sub(r'\( \)', '', string)
    string = re.sub(r'\(  \)', '', string)
    string = re.sub(r'\(   \)', '', string)
    string = re.sub(r'\(\ \)', '', string)
    string = re.sub(r'\(\ \ \)', '', string)
    string = re.sub(r'\(\ \ \ \)', '', string)
    # dont want to test more compelx regex for this
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

    if not re.match(r'.*\.mp3', str(filepath)):
        return

    # Create a temporary name for the current file, mp3 only!
    # i.e: 'sound.mp3' -> 'sound_temp.mp3'
    temp_filepath = filepath[:len(filepath) - len('.mp3')] + '_temp' + '.mp3'

    # Rename the file to the temporary name.
    Path(filepath).replace(Path(temp_filepath))

    # Run the ffmpeg command to copy this file.
    # This fixes the duration and creates a new file with the original name.
    command = 'ffmpeg -v quiet -i "' + temp_filepath + \
        '" -acodec copy "' + filepath + '"'
    os.system(command)

    # Remove the temporary file that had the wrong duration in its metadata.
    Path(temp_filepath).unlink()


def clean(filepath, config):
    # "only clean music metadata"
    ok_extension = False
    for ext in config.valid_extensions:
        ok_extension |= filepath.endswith(ext)
    if not ok_extension:
        return

    audio = music_tag.load_file(str(Path(filepath)))
    title = audio["title"].value
    artist = audio["artist"].value  # only consider first tag if there is many

    audio["title"] = cleanstr(title, config)
    audio["artist"] = cleanstr(artist, config)

    audio.save()

    # if mp3, fix length issue: no quality is lost by re-encode but
    # bitrate and length will be fixed
    if re.match(r'.*\.mp3', str(filepath)):
        fix_duration(filepath)
