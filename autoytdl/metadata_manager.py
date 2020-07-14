#!/bin/env python3

from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from sys import argv
import os
from math import floor
from mutagen.mp3 import MP3


def openmp3(filepath):
    # Create MP3File instance.
    mp3 = MP3File(filepath)
    mp3.set_version(VERSION_2)
    # Get/set/del tags value.
    title = mp3.song.rstrip('\x00')
    artist = mp3.artist.rstrip('\x00')
    audio = MP3(filepath)
    length = floor(audio.info.length)
    return (title, artist, length)


def openlist(path_to_metadata):
    if not os.path.exists(path_to_metadata):
        os.system("touch " + path_to_metadata)
    fichier = open(path_to_metadata, "r")
    list_tags = set(fichier.readlines())
    fichier.close()
    return list_tags


def append_to_file(tuple_mp3, path_to_metadata):
    fichier = open(path_to_metadata, "a")
    fichier.write(str(tuple_mp3) + "\n")
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


def inlist(mp3_tuple, liste):
    for x in liste:
        if equal(eval(x), mp3_tuple):
            return True
    return False


def can_be_music(mp3_tuple, config):
    return mp3_tuple[0] != "" and mp3_tuple[1] != "" and mp3_tuple[2] >= config.min_length and mp3_tuple[2] <= config.max_length


def should_add(mp3_file, config):
    list_tags = openlist(config.path_to_metadata)

    instancemp3 = list(openmp3(mp3_file))

    if not can_be_music(instancemp3, config) and not config.force:
        print("[probably not a music file, not adding] ", tuple(instancemp3))
        return False

    for i in range(len(instancemp3)):
        instancemp3[i] = str(significant_words(str(instancemp3[i])))
    tuple_mp3 = tuple(instancemp3)

    if inlist(tuple_mp3, list_tags) and not config.force:
        print("[already present in metadata archive, skipping]", tuple_mp3)
        return False
    else:
        print("[adding to metadata archive]", tuple_mp3)
        append_to_file(tuple_mp3, config.path_to_metadata)
        return True
