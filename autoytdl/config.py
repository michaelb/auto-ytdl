from pathlib import Path, PurePath
import tempfile
import os
import toml
from datetime import date
from autoytdl.version import __version__


class Config:

    def __init__(self):
        # defaults parameters
        path_to_home = str(Path.home())
        temp_dir = tempfile.TemporaryDirectory()
        if not os.path.exists(path_to_home+"/.config"):
            os.makedirs(path_to_home+"/.config")
        if not os.path.exists(path_to_home+"/.config/auto-ytdl"):
            os.makedirs(path_to_home+"/.config/auto-ytdl")
        # cahne from musictest to real Music folder
        if not os.path.exists(path_to_home+"/Music"):
            os.makedirs(path_to_home+"/Music")

        self.version = __version__
        self.config_directory = str(Path.home())+"/.config/auto-ytdl/"
        self.library_path = str(PurePath(Path.home(), "Music/"))
        self.path_to_metadata = self.config_directory + "metadata_archive.txt"
        self.temp_dir = temp_dir
        self.clean_exit = True
        self.pre_command = ""
        self.post_command = ""
        self.valid_extensions = [".mp3", ".ogg",
                                 ".opus", ".flac", ".aac", ".m4a"]

        self.denylist_names = ["Release", "Music", "Lyric", "Radio",
                               "Recording", "Premiere", "Audio",
                               "Exclusive", "Video", "Official"]
        self.url_list = []
        self.force = False
        self.min_length = 60
        self.max_length = 600
        self.youtube_dl_args = {"ignore-errors": True,
                                "max-downloads": 500,
                                "quiet": False,
                                "download-archive": self.config_directory + "archive.txt",
                                "dateafter": date.today().strftime("%Y%m%d"),
                                "metadata-from-title": "\"%(artist)s - %(title)s\"",
                                "output": "\"" + self.temp_dir.name + "/%(title)s.%(ext)s\"",
                                "add-metadata": True,
                                "force-ipv4": True,
                                "extract-audio": True,
                                "audio-format": False,
                                "no-continue": True,
                                "audio-quality": 0,
                                "embed-thumbnail": False,
                                "playlist-end": 150}

    def reset_soft(self):
        # backup
        self.write(str(Path.home())+"/.config/auto-ytdl/config.toml.backup")
        # restore default config but try to keep some user changes
        clean = Config()
        # values to preserve
        for key in ["config_directory", "library_path", "path_to_metadata", "clean_exit", "pre_command", "post_command", "denylist_names", "min_length", "max_length", "url_list", "valid_extensions"]:
            clean.__dict__[key] = self.__dict__[key]

        # values of youtube_dl_args to preserve
        for ytkey in ["max-downloads", "dateafter", "playlist-end"]:
            clean.__dict__["youtube_dl_args"][ytkey] = self.__dict__[
                "youtube_dl_args"][ytkey]

        self = clean
        self.write()

    def load(self):
        # check if config file already present, if so load it, else create it
        config_file_path = self.config_directory+"config.toml"
        if os.path.isfile(config_file_path):
            config_dict = toml.load(config_file_path)
            self.__dict__ = config_dict

            # check if no major version change
            # no exception if there is no self.version as 'or' short-circuit
            if ("version" not in config_dict) or config_dict["version"][0] < __version__[0]:
                raise Exception("Major version change")

            self.temp_dir = tempfile.TemporaryDirectory()
            self.youtube_dl_args["output"] = "\"" + \
                self.temp_dir.name + "/%(title)s.%(ext)s\""
            if not self.clean_exit:
                # so evertyhing will be way slower next time but
                # we will not miss any music
                os.system("rm -f " + self.config_directory+"archive.txt")
            self.write()
        else:
            self.write()

    def write(self, path=str(Path.home())+"/.config/auto-ytdl/config.toml"):
        config_file_path = path
        with open(config_file_path, "w+") as f:
            to_write = vars(self)
            f.write(toml.dumps(to_write))

            f.write("#Delete this file to restore defaults\n\n\n")
            f.write("\n\n  # A quick explanation for every useful,\n\
                    # user-modifiable option:\n\n\
                    # other options are not intended\n\
                    # to be modified by the user\n\n\n\
                     # -library_path : path to your music library.\n\
                    # auto-ytdl will dump mp3 files there.\n\
                    # -pre/post command: shell command to run\n\
                            # before/after aytl commands. Can be\n\
                            # useful for stopping your music player\n\
                            # or telling it to rescan your library\n\
                    # - denylist_names: an array of things you\n\
                            # don't want in your music metadata.\n\
                            # Matches also lowercase and plural, so\n\
                            # adding \"Lyric\" will ensure that the\n\
                            # video \"Rick Astley - Never Gonna Give \n\
                            # You Up (lyrics)\" will be tagged\n\
                            # \"Rick Astley\" and\n\
                            # \"Never Gonna Give You Up\"\n\
                    # -min/max length (seconds): will not add \n\
                            # shorter/longer music to your library,\n\
                            # unless --force is used\n\
                    # - url_list: list of artist you've added.\n\
                            # You should use add/remove and not\n\
                            # modify this directly, but you can\n\
                    # - youtube_dl_args: youtube-dl '--' args: \n\
                            # You can add above your own --options\n\
                            # for youtube-dl, without the\n\
                            # double dash.\n\
                            # Write: 'option = true' for flags \n\
                            # that do not take arguments,\n\
                            # 'option = value' otherwise.\n\
                            # option = false will disable it.\n\
                            # Don't forget to wrap string\n\
                            # values in \"\" quotes\n\n\n\
                            # for example, setting\n\
                            #audio-format=\"mp3\" is correct syntax\n\
                            # \n\
                            # max downloads: max downloads at once\n\
                            # will abort if more downloads are\n\
                            # attempted as this will understood as\n\
                            # a potentially disastrous user error \n\
                            # should so much (maybe unintended)\n\
                            # titles be added to the user's library\n\
                            # \n\
                            # playlist-end : 150 means that you \n\
                            # will not download more that 150\n\
                            # titles of one source. You can modify\n\
                            # it to any arbitraty high integer,\n\
                            # but your the pre-download step\n\
                            # will be much slower\n")
