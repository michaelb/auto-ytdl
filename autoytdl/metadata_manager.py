#!/bin/env python3

from sys import argv
import os
from math import floor

import music_tag
import mutagen


def openaudio(filepath):
    # Create MP3File instance.
    audio = music_tag.load_file(filepath)
    # Get/set/del tags value.
    title = audio["title"].value.rstrip('\x00')
    artist = audio["artist"].value.rstrip('\x00')
    audio2 = mutagen.File(filepath)
    length = floor(audio2.info.length)
    return (title, artist, length)


def openlist(path_to_metadata):
    if not os.path.exists(path_to_metadata):
        os.system("touch " + path_to_metadata)
    fichier = open(path_to_metadata, "r")
    list_tags = set(fichier.readlines())
    fichier.close()
    return list_tags


def append_to_file(tuple_audio, path_to_metadata):
    fichier = open(path_to_metadata, "a")
    fichier.write(str(tuple_audio) + "\n")
    fichier.close()


def equal(m1, m2):
    i = 1
    if m1[0] == m2[0]:
        i = i * 10
    if m1[1] == m2[1]:
        i = i * 10

    if abs(float(m2[2]) - float(m1[2])) < 15:
        i = i * 4

    if m1[1] in m2[1]:
        i = i*5
    if m2[1] in m1[1]:
        i = i*5
    if m1[0] in m2[0]:
        i = i*5
    if m2[0] in m1[0]:
        i = i*5
    if "remix" in m1[0].lower() != "remix" in m2[0].lower():
        i = i / 5
    if "remix" in m1[1].lower() != "remix" in m2[1].lower():
        i = i / 5
    return i > 2500


def alphanumeric(string):
    return string.isalpha or string.isdigit


def significant_words(text):
    L = text.split(' ')
    for i in range(len(L)):
        L[i] = ''.join(filter(alphanumeric, L[i]))
        L[i] = L[i].lower()
    L2 = []
    for x in L:
        if len(x) > 2:
            L2.append(x)
    string = ""
    for x in L2:
        string += x
    return string


def inlist(audio_tuple, liste):
    for x in liste:
        if equal(eval(x), audio_tuple):
            return True
    return False


def can_be_music(audio_tuple, config):
    return audio_tuple[0] != "" and audio_tuple[1] != "" and audio_tuple[2] >= config.min_length and audio_tuple[2] <= config.max_length


def should_add(filepath, config):
    list_tags = openlist(config.path_to_metadata)

    instanceaudio = list(openaudio(filepath))

    if not can_be_music(instanceaudio, config) and not config.force:
        print("[probably not a music file, not adding] ", tuple(instanceaudio))
        return False

    for i in range(len(instanceaudio)):
        instanceaudio[i] = str(significant_words(str(instanceaudio[i])))
    tuple_audio = tuple(instanceaudio)

    if inlist(tuple_audio, list_tags) and not config.force:
        print("[already present in metadata archive, skipping]", tuple_audio)
        return False
    else:
        if not inlist(tuple_audio, list_tags):
            print("[adding to metadata archive]", tuple_audio)
            append_to_file(tuple_audio, config.path_to_metadata)
        return True
