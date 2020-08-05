from pathlib import Path
import tempfile
import os
import platform
import toml
from datetime import date
from autoytdl.version import __version__


class Config:

    def __init__(self):
        # defaults parameters
        path_to_home = str(Path.home())
        temp_dir = tempfile.TemporaryDirectory()

        if platform.system() == "Linux" or platform.system() == "Darwin":
            config_dir = ".config"
        elif platform.system() == "Windows":
            config_dir = "Documents"
        else:
            raise Exception("Unsupported platform")

        # create various path if they do not exit
        Path(path_to_home+"/" + config_dir).mkdir(parents=True, exist_ok=True)
        Path(path_to_home+"/" + config_dir +
             "/auto-ytdl").mkdir(parents=True, exist_ok=True)
        # check if default library folder exists
        Path(path_to_home+"/Music").mkdir(parents=True, exist_ok=True)

        # ORDER OF COMMENTS AND OPTIONS IS PARAMOUNT TO CORRECT COMMENTS IN CONFIG FILE

        self.comments = ["Software version"]
        self.version = __version__

        self.comments += ["Path to the config directory"]
        self.config_directory = str(
            Path(str(Path.home())+"/"+config_dir+"/auto-ytdl"))

        self.comments += ["Path to the user's music library"]
        self.library_path = str(str(Path.home()) + "/Music")

        self.comments += ["Path to the metadata archive"]
        self.path_to_metadata = self.config_directory + "/metadata_archive.txt"

        self.comments += ["Not user modifiable. Directory to store temporary files"]
        self.temp_dir = temp_dir

        self.comments += ["Whether the last program exit was 'clean' or aborted; the next program run will be much longer if false"]
        self.clean_exit = True

        self.comments += ["Command to run before auto-ytdl starts"]
        self.pre_command = ""

        self.comments += [
            "Command to run after auto-ytdl exit (refreshing/rescanning library of your music player?)"]
        self.post_command = ""

        self.comments += [
            "Extensions supported by your music player, add or remove any you think is rigth"]
        self.valid_extensions = [".mp3", ".ogg",
                                 ".opus", ".flac", ".aac", ".m4a"]

        self.comments += [
            "Words you do NOT want in song's metadata. So a video named \"Queen - Bohemian Rhapsody (Official video) (lyrics)\" becomes a music tagged \"Queen\" and \"Bohemian Rhapsody\" "]
        self.denylist_names = ["Release", "Music", "Lyric", "Radio",
                               "Recording", "Premiere", "Audio",
                               "Exclusive", "Video", "Official", "High Definition"]

        self.comments += [
            "urls of added channels/playlists. Please use the add/remove/list interface to modify"]
        self.url_list = []

        self.comments += ["Not user modifiable"]
        self.force = False

        self.comments += [
            "Minimum length (in seconds) a music must have to be moved into the user's library (discarded otherwise)"]
        self.min_length = 60

        self.comments += [
            "Maximum length (in seconds) a music must have to be moved into the user's library (discarded otherwise)"]
        self.max_length = 600

        self.comments += [
            "Embed thumbnail when possible (for opus and mp3 format)"]
        self.embed_thumbnail = True

        # youtube-dl args section
        self.comments += [""]  # padding
        self.comments += [
            "youtube-dl arguments: double-dash \"--\" arguments may be appended at the END of the config file:\n#write: \"option name without --\" = true/false/value\n#-> true to activate a flag\n#-> false to make it not appear in the command\n#-> value (or \"value\" for string values) to set the option argument"]
        self.comments += ["Don't stop downloading if one of many downloads had an error"]
        self.comments += [
            "Never download more than this much at once (prevent mistakes)"]
        self.comments += ["No ouptput from youtube-dl"]
        self.comments += ["Not user modifiable"]
        self.comments += ["Date (yyyymmdd) of last download, can be user modified, but not on a regular basis. Changing this will make auto-ytdl think you don't have updated since %dateafter"]
        self.comments += ["Should really not be modified, as most of the video naming follow this convention, unless you know what you are doing"]
        self.comments += ["Temp directory, not user-modifiable"]
        self.comments += ["Don't set to false unless you don't want title/artist metadata"]
        self.comments += [
            "can be toggled true/false if you encounter youtube-dl err 429 (too much consecutive downloads"]
        self.comments += ["Not user modifiable"]
        self.comments += [
            "Ideally, should only be \"best\" (default) or \"mp3\" so the eventual thumbnail is correctly embedded most of the time (opus and mp3 format are the main focus of dev)"]
        self.comments += ["You should not change this"]
        self.comments += ["Not user modifiable"]
        self.comments += ["Do not download more than this much music from one source"]
        self.youtube_dl_args = {"ignore-errors": True,
                                "max-downloads": 500,
                                "quiet": False,
                                "download-archive": self.config_directory + "/archive.txt",
                                "dateafter": date.today().strftime("%Y%m%d"),
                                "metadata-from-title": "\"%(artist)s - %(title)s\"",
                                "output": "\"" + self.temp_dir.name + "/%(title)s.%(ext)s\"",
                                "add-metadata": True,
                                "force-ipv4": True,
                                "extract-audio": True,
                                "audio-format": "best",
                                "audio-quality": 0,
                                "write-thumbnail": True,
                                "playlist-end": 150}

    def reset_soft(self):
        # backup
        self.write(str(Path.home())+self.config_directory +
                   "/config.toml.backup")
        # restore default config but try to keep some user changes
        clean = Config()
        # values to preserve
        for key in ["config_directory", "library_path", "path_to_metadata", "clean_exit", "pre_command", "post_command", "denylist_names", "min_length", "max_length", "url_list", "valid_extensions", "embed_thumbnail"]:
            if key in self.__dict__:
                clean.__dict__[key] = self.__dict__[key]

        # values of youtube_dl_args to preserve
        for ytkey in ["max-downloads", "dateafter", "playlist-end"]:
            if ytkey in self.__dict__:
                clean.__dict__["youtube_dl_args"][ytkey] = self.__dict__[
                    "youtube_dl_args"][ytkey]

        self = clean
        self.write()

    def load(self):
        # check if config file already present, if so load it, else create it
        config_file_path = self.config_directory+"/config.toml"

        # because we don't want to save comments as a option in config file, need to pass it from default
        comment_save = self.comments.copy()
        if Path(config_file_path).exists():
            config_dict = toml.load(config_file_path)
            self.__dict__ = config_dict
            self.__dict__["comments"] = comment_save

            # check if no major version change
            # no exception if there is no self.version as 'or' short-circuit
            if ("version" not in config_dict) or config_dict["version"][0] < __version__[0]:
                raise Exception("Major version change")

            self.temp_dir = tempfile.TemporaryDirectory()
            self.youtube_dl_args["output"] = "\"" + \
                str(Path(self.temp_dir.name + "/%(title)s.%(ext)s")) + "\""
            if not self.clean_exit:
                # so evertyhing will be way slower next time but
                # we will not miss any music
                Path(self.config_directory+"/archive.txt").unlink()
            self.write()
        else:
            print("Hey! It looks like it's the first time you are using auto-ytdl.\nYou may want to see the help menu and edit the configuration to suit your needs!\n\n\n")
            self.write()

    def write(self, path=""):
        if path == "":
            path = str(Path(self.config_directory + "/config.toml"))

        config_file_path = path
        with open(config_file_path, "w+") as f:

            coms = Config().comments.copy()

            to_write = vars(self)
            comments_save = to_write.pop("comments", None)
            conf = toml.dumps(to_write).splitlines()
            self.__dict__["comments"] = comments_save

            # pad so lack of comment does not suppress options because of zip length mismatch
            if len(conf) > len(coms):
                coms.extend([""] * (len(conf) - len(coms)))

            f.write(
                "#This is the config file for auto-ytdl.\n#To reset auto-ytdl to defaults, you can entirely delete this file.\n\n")
            for option, explication in zip(conf, coms):
                f.write("# "+explication+"\n")
                f.write(option + "\n")
                f.write("\n")

            f.write("#PUT YOUR YOUTUBE-DL \"--\" OPTIONS / OPTION-ARGUMENTS BELOW\n")
            f.write("# (note that comments will be removed; it allows me to easily update this config file, without breaking too much your changes)")
