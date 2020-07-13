import sys
import os
import re
from pathlib import Path, PurePath
from autoytdl.config import Config
from autoytdl.arguments import get_args


class AYTDL:
    def __init__(self):
        self.config = Config()
        self.config.load()

        self.args = get_args()

    def update(url, dateafter):
        print("Not implemeted yet")


def is_url(string):
    youtube_channel_regex = "(https?: \/\/)?(www\.)?youtu((\.be) | (be\..{2, 5}))\/((user) | (channel))\/"
    if re.match(youtube_channel_regex, string):
        return True
    else:
        answer = input("Warning:\n" + string + "\nThe provided url \
does not look like a typical youtube channel \
url, add it anyway? [Y/n]:")
        if answer == "Y" or answer == "y" or answer == "Yes"\
                or answer == "yes" or answer == "":
            return True
    return False


def main():
    a = AYTDL()
    command = a.args.get("COMMANDS")

    if command == "update":
        urls_to_update = a.args.get("update")
        dateafter = 19600101
        if not urls_to_update:  # list is empty
            urls_to_update = a.config.url_list
            dateafter = a.config.date.youtube_dl_args.get('dateafter')
        for url in urls_to_update:
            a.update(urls_to_update, dateafter)

        # TODO update date

    elif command == "add":
        for url in a.args.get("add"):
            if is_url(url) and url not in a.config.url_list:
                a.config.url_list.append(url)
                print("[added] "+url)
            else:
                print("[not added] "+url)
        a.config.write()

    elif command == "remove":
        for url in a.args.get("remove"):
            if url in a.config.url_list:
                a.config.url_list.remove(url)
                print("[removed] " + url)
            else:
                print("[not found] " + url)
        a.config.write()

    elif command == "list":
        for url in a.config.url_list:
            print(url)

    elif command == "edit":
        config_file_path = str(Path.home())+"/.config/auto-ytdl/config.toml"
        os.system("xdg-open " + config_file_path)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
