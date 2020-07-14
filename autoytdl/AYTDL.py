import sys
import os
import re
import tempfile
import shutil
from pathlib import Path
from datetime import date
from autoytdl.config import Config
from autoytdl.arguments import get_args
from autoytdl.metadata_manager import should_add
from autoytdl.name_cleaner import clean


class AYTDL:
    def __init__(self):
        self.config = Config()
        self.config.load()

        self.args = get_args()

    def download_to_temp(self, url, dateafter):
        def prepare_ytdl_commmand_line(dateafter):
            line = ""
            for key, value in self.config.youtube_dl_args.items():
                if key == "datefater":
                    continue
                line += " "
                if value is True:
                    line += "--" + key
                elif value is False:
                    pass
                else:
                    line += "--" + key + " " + str(value)
            # special case because it is updated or not for
            line += " --dateafter " + str(dateafter)
            return line
        exit_code = os.system("youtube-dl " +
                              prepare_ytdl_commmand_line(dateafter) + " " + url)
        if exit_code != 0:
            self.config.clean_exit = False
            self.config.write()
            sys.exit(exit_code)

    def clean_tags(self):
        temp_dir_path = self.config.temp_dir.name
        for filename in os.listdir(temp_dir_path):
            clean(temp_dir_path+"/" + filename, self.config)

    def move_to_library(self):
        temp_dir_path = self.config.temp_dir.name
        for filename in os.listdir(temp_dir_path):
            if filename.endswith(".mp3") and not filename.endswith(".temp.mp3"):
                # this manage the metadata archive
                if should_add(temp_dir_path+"/"+filename, self.config):
                    # use ffmpeg to copy as it also solve a wrong song length problem
                    os.system("mv " + "'"+temp_dir_path+"/" + filename + "'" +
                              " " + "'" + self.config.library_path + "/" + filename+"'")


def is_url(string):
    youtube_channel_regex = "(https?://)?(www.)?youtu((.be)|(be..{2,5}))/((user)|(channel))/"
    if re.match(youtube_channel_regex, string):
        return True
    else:
        answer = input("Warning:\n" + string + "\nThe provided url \
does not look like a typical youtube channel \
url, add it anyway? [Y/n]:")
        if answer == "Y" or answer == "y" or answer == "Yes" or answer == "yes" or answer == "":
            return True
    return False


def main():
    a = AYTDL()
    command = a.args.get("COMMANDS")

    if command == "update":
        urls_to_update = a.args.get("update")
        if not type(urls_to_update) is list:
            urls_to_update = [urls_to_update]
        dateafter = a.config.youtube_dl_args.get('dateafter')
        if not urls_to_update:  # list is empty
            urls_to_update = a.config.url_list
        if a.args.get("include_old"):
            dateafter = 19600101
        if a.args.get("force"):
            a.config.force = True

        for url in urls_to_update:
            a.download_to_temp(url, dateafter)

        a.clean_tags()
        a.move_to_library()
        a.config.youtube_dl_args["dateafter"] = date.today().strftime("%Y%m%d")

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

    # cleanup
    shutil.rmtree(a.config.temp_dir.name)
    a.config.clean_exit = True
    a.config.force = False
    a.config.write()


if __name__ == "__main__":
    main()
