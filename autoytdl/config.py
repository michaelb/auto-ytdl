from pathlib import Path, PurePath
import tempfile
import os
import toml


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
        if not os.path.exists(path_to_home+"/Musictest"):
            os.makedirs(path_to_home+"/Musictest")

        config_directory = str(Path.home())+"/.config/auto-ytdl/"
        self.library_path = str(PurePath(Path.home(), "Musictest/"))
        self.path_to_metadata = config_directory + "metadata_archive.txt"
        self.temp_dir = temp_dir
        self.clean_exit = True

        self.denylist_names = ["Proximity", "Diversity", "Release", "Music", "Lyric",
                               "Radio", "Recording", "Premiere", "Audio", "Exclusive"]
        self.url_list = []
        self.force = False
        self.min_length = 60
        self.max_length = 600
        self.youtube_dl_args = {"ignore-errors": True,
                                "max-downloads": 5,
                                "quiet": False,
                                "download-archive": config_directory + "archive.txt",
                                "dateafter": "19600101",
                                "metadata-from-title": "\"%(artist)s - %(title)s\"",
                                "output": "\"" + self.temp_dir.name + "/%(title)s.%(ext)s\"",
                                "add-metadata": True,
                                "extract-audio": True,
                                "audio-format": "mp3",
                                "no-continue": True,
                                "audio-quality": 0,
                                "embed-thumbnail": False,
                                "playlist-end": 3}

    def load(self):
        # check if config file already present, if so load it, else create it
        config_file_path = str(Path.home())+"/.config/auto-ytdl/config.toml"
        if os.path.isfile(config_file_path):
            config_dict = toml.load(config_file_path)
            self.__dict__ = config_dict
            # TODO check if temp dir exist or is empty
            self.temp_dir = tempfile.TemporaryDirectory()
            self.youtube_dl_args["output"] = "\"" + \
                self.temp_dir.name + "/%(title)s.%(ext)s\""
            if not self.clean_exit:
                # so evertyhing will be way slower next time but we will not miss any music
                os.system("rm " + str(Path.home()) +
                          "/.config/auto-ytdl/archive.txt")
            self.write()
        else:
            self.write()

    def write(self):
        config_file_path = str(Path.home())+"/.config/auto-ytdl/config.toml"
        with open(config_file_path, "w+") as f:
            to_write = vars(self)
            f.write(toml.dumps(to_write))
            f.write("#\n#You can add above your own --options for youtube-dl, without the double dash. \n#Write: 'option = true' for flags that do not take arguments, 'option = value' otherwise. \n#Don't forget to wrap string values in \"\" quotes")
