from pathlib import Path, PurePath
import os
import toml


class Config:
    def __init__(self):
        # defaults parameters
        path_to_home = str(Path.home())
        if not os.path.exists(path_to_home+"/.config"):
            os.makedirs(path_to_home+"/.config")
        if not os.path.exists(path_to_home+"/.config/auto-ytdl"):
            os.makedirs(path_to_home+"/.config/auto-ytdl")
        # cahne from musictest to real Music folder
        if not os.path.exists(path_to_home+"/Musictest"):
            os.makedirs(path_to_home+"/Musictest")

        config_directory = str(Path.home())+"/.config/auto-ytdl/"
        self.library_path = str(PurePath(Path.home(), "Musictest"))
        self.use_metadata_archive = True
        self.metadata_archive_path = config_directory + "metadata_archive.txt"
        self.auto_update_frequency = 0
        self.url_list = {"1", "2", "3"}
        self.youtube_dl_args = {"ignore-errors": True,
                                "max-downloads": 150,
                                "max-filesize": "15M",
                                "quiet": True,
                                "path-to-archive": config_directory + "archive.txt",
                                "dateafter": "19600101",
                                "metadata-from-title": "%(artist)s - %(title)s",
                                "output": self.library_path + "%(tilte)s.%(ext)s",
                                "add-metadata": True,
                                "extract-audio": True,
                                "audio-format": "mp3",
                                "no-continue": True,
                                "output-format": "mp3",
                                "audio-quality": 0,
                                "embed-thumbnail": True,
                                "playlist-end": 100}

    def write_to_file(self):
        config_file_path = str(Path.home())+"/.config/auto-ytdl/config.toml"
        with open(config_file_path, "w+") as f:
            to_write = self.__dict__
            f.write(toml.dumps(to_write))
