import sys
import os
import re
import shutil
import tempfile
import subprocess
try:
    from pathlib import Path
    from datetime import date
    import music_tag
    import mutagen
    import argparse
    import toml
except Exception:
    print("Fetching auto-ytdl pip dependencies. (install as --user)")
    os.system(
        "pip install --user pathlib datetime music_tag mutagen argparse toml")
    print("Done, please re-launch auto-ytdl")
    sys.exit(0)

from autoytdl.config import Config
from autoytdl.arguments import get_args
from autoytdl.metadata_manager import should_add
from autoytdl.name_cleaner import clean
from autoytdl.thumbnail_embedder import embed_mp3, embed_opus


class AYTDL:
    def __init__(self):
        self.config = Config()
        try:
            self.config.load()
        except Exception as inst:
            if str(inst) == "Major version change":
                print("\033[91mWarning: " + str(inst) + "\033[0m")
                print("A major version has been changed, and your configuration  was changed:\n - options were added\n - some may have been reset.\n\nYour old configuration file has been saved at " +
                      self.config.config_directory + "config.toml.backup\n\nI recommend to have a quick look at the new configuration to check if everything is alright.\nYou can do so via \"aytdl edit\"")
                self.config.reset_soft()
                sys.exit(0)

            # if not a major version change, really bad problem with the config
            print("Bad configuration file, you may want to check syntax. Delete the configuration file to reset to defaults")
            sys.exit(1)

        self.args = get_args()

    def download_to_temp(self, url, dateafter):
        def prepare_ytdl_commmand_line(dateafter):
            line = ""
            for key, value in self.config.youtube_dl_args.items():
                if key == "datefater" or key == "download-archive":
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
            # special case 2 to ignore archive
            if not self.config.force:
                line += " --download-archive " + \
                    self.config.youtube_dl_args["download-archive"] + " "

            return line

        # in case url contains special shell symbols
        if not ((url[0] == "\"" or url[0] == "'") and (url[-1] == "'" or url[-1] == "\"")):
            url = "\""+url+"\""

        # here we run youtube-dl
        exit_code = os.system("youtube-dl " +
                              prepare_ytdl_commmand_line(dateafter) + " " + url)
        if exit_code != 0:  # may be a youtube-dl error taht is recoverable
            ask = "Y"
            if not self.config.force:
                ask = input("Error code: " + str(exit_code) +
                            "\nyoutube-dl encountered at least one error.\nThat can happen when a video you are trying to download is not-standart (geo-restricted, not released yet, 'première').\nContinue anyway (recommended: yes) ? (Y/n): ")
            if ask == "N" or ask == "n" or ask == "No" or ask == "no":
                self.config.clean_exit = False
                self.config.write()
                sys.exit(exit_code)

    def clean_tags(self):
        def ok(filename):
            for ext in self.config.valid_extensions:
                if filename.endswith(ext):
                    return True
            return False
        temp_dir_path = self.config.temp_dir.name
        for filename in os.listdir(temp_dir_path):
            if ok(filename) and not filename.endswith(".temp.mp3"):
                clean(temp_dir_path+"/" + filename, self.config)

    def embed_thumbnail(self):

        temp_dir_path = self.config.temp_dir.name
        for filename in os.listdir(temp_dir_path):
            # MP3 files
            if filename.endswith(".mp3") and not filename.endswith(".temp.mp3"):
                embed_mp3(temp_dir_path, filename)

            # OPUS files
            if filename.endswith(".opus") and not filename.endswith(".temp.opus"):
                embed_opus(temp_dir_path, filename)

    def move_to_library(self):
        def ok(filename):
            for ext in self.config.valid_extensions:
                if filename.endswith(ext):
                    return True
            return False

        temp_dir_path = self.config.temp_dir.name
        for filename in os.listdir(temp_dir_path):
            if ok(filename) and not filename.endswith(".temp.mp3"):
                # this manage the metadata archive
                if should_add(temp_dir_path+"/"+filename, self.config):
                    # use ffmpeg to copy as it also solve a wrong song length problem
                    print("[moving to library] " + filename)
                    shutil.move("\"" + temp_dir_path+"/" + filename + "\"",
                                "\""+self.config.library_path + "/" + filename+"\"")


# ##END OF AYTDL CLASS

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
    a.config.clean_exit = False  # will be reset to true at the programm end
    a.config.write()  # so in case of premature exit, clean_exit is false

    # pre-command
    if a.config.pre_command != "":
        print("[running pre_command] " + a.config.pre_command)
        exit_code = os.system(a.config.pre_command)
        if exit_code != 0:
            sys.exit(exit_code)

    command = a.args.get("COMMANDS")

    # UPDATE COMMAND
    if command == "update":
        urls_to_update = a.args.get("update")
        dateafter = a.config.youtube_dl_args.get('dateafter')

        # flag to check if potentially dangerous -i or -f, and decide if date update
        full_update = False
        if not type(urls_to_update) is list:
            urls_to_update = [urls_to_update]
        # list is empty, full update
        if not urls_to_update and not a.args.get("playing"):
            full_update = True
            # check if date is today so to not lose time
            if a.config.youtube_dl_args["dateafter"] == date.today().strftime("%Y%m%d") and not a.args.get("force") and not a.args.get("include_old") and not a.args.get("playing"):
                print("Already up to date, nothing to do")
                return 0
            urls_to_update = a.config.url_list
            if not urls_to_update:
                print("Your list of music sources is empty, you may want to \"add\" your favorite youtube channels, playlists, or other sources")
                sys.exit(0)

        # --playing should always download even if old,
        # thus it implies include-old
        if a.args.get("include_old") or a.args.get("playing"):
            dateafter = 19600101
            # playing remove urls to update anyway
            if full_update and not a.args.get("playing"):
                ask = input("Looks like you are trying to run a full update with --include-old flag. This will download up to (config:playlist-end) " +
                            str(a.config.youtube_dl_args["playlist-end"]) + " songs from each source.\nAre you sure you want to do this? [y/N]:")
                if ask == "y" or ask == "Y" or ask == "Yes" or ask == "yes":
                    print("This may take a long time, starting now...")
                else:
                    sys.exit(0)

        # force is a real FORCE and thus implies include-old
        if a.args.get("force"):
            a.config.force = True
            dateafter = 19600101
            if full_update and not a.args.get("playing"):
                ask = input("Looks like you are trying to run a full update with the --force flag. This will download up to (config:playlist-end) "+str(
                    a.config.youtube_dl_args["playlist-end"]) + " songs from each source, including songs you have are downloaded (true duplicates will not be added).\nAre you sure you want to do this? [y/N]:")
                if ask == "y" or ask == "Y" or ask == "Yes" or ask == "yes":
                    print("This may take a long time, starting now...")
                else:
                    sys.exit(0)

        if a.args.get("playing"):
            urls_to_update = []

            current = subprocess.check_output(
                "strings \""+str(Path.home())+"/.config/google-chrome/Default/Current Session\" | grep -E \"^https?://www.youtube\"  | tail -1", shell=True)
            if current != b'' and current != '':
                urls_to_update = [str(current)[2:-3]]

        # download for real
        for url in urls_to_update:
            print("[downloading] " + url)
            a.download_to_temp(url, dateafter)

        if a.config.embed_thumbnail:
            a.embed_thumbnail()
        a.clean_tags()
        a.move_to_library()
        if full_update:
            a.config.youtube_dl_args["dateafter"] = date.today().strftime(
                "%Y%m%d")

    # ADD COMMAND
    elif command == "add":
        for url in a.args.get("add"):
            if is_url(url) and url not in a.config.url_list:
                a.config.url_list.append(url)
                print("[added] "+url)
            else:
                print("[not added] "+url)
        a.config.write()

    # REMOVE COMMAND
    elif command == "remove":
        for url in a.args.get("remove"):
            if url in a.config.url_list:
                a.config.url_list.remove(url)
                print("[removed] " + url)
            else:
                print("[not found] " + url)
        a.config.write()

    # LIST COMMAND
    elif command == "list":
        for url in a.config.url_list:
            print(url)

    # EDIT COMMAND
    elif command == "edit":
        config_file_path = str(Path(a.config.config_directory+"/config.toml"))
        os.system("xdg-open " + config_file_path)
    else:
        print("Invalid command")

    # cleanup
    shutil.rmtree(a.config.temp_dir.name)
    a.config.temp_dir = ""
    a.config.clean_exit = True
    a.config.force = False
    a.config.write()

    # post-command
    if a.config.post_command != "":

        print("[running post_command] " + a.config.post_command)
        exit_code = os.system(a.config.post_command)
        if exit_code != 0:
            sys.exit(exit_code)


if __name__ == "__main__":
    main()
