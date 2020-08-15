While there is no (yet?) test framework, this should cover the necessities to ensure all advertised features of auto-ytdl work:

## Do the program looks ok?
0.1 : do the program run ?
0.2 : do 'aytdl --help' and 'aytdl --version' display a sensible output
0.3 : do running aytdl without args gives a understandable error and explication?

## Does it setup correctly?
1.0 : After running aytdl for the first time, missing dependencies should have been pulled for the first time, and the program should exit without running the specified command. Did it work?
1.1 : After running aytdl for the second time, config directory and files should have been created. (in .config/auto-ytdl for Unix platform, Documents/auto-ytdl for windows). Do config.toml looks correct (non-empty, comments next to their options)?


## Does the commands add, remove, list and edit work?
2.0 : you should test that by adding youtube channels and random url, then listing to configm they've appeared, then removing them, then listing the remainder. Did it work?
2.1: aytdl edit should open the default text editor on Unix platforms and Notepad on windows with the config.toml file preloaded. You should be able to edit it rigth away, is it rigth?

## Update command
3.0.0: do aytl update <urls> works as expected for youtube unique videos? (is a music file put in the config:library\_path folder)?
3.0.1 : if trying to redownload an already downloaded video, is this catched by the archive? Can it be bypassed by using --force?
3.0.2: if you remove the archive in the config folder, and try to re-download the same video, is it still skipped by the metadata-archive?
3.1.0: do 'aytdl update <youtube-channel-url> --include-old' works as expected (download all, up to config:playlist-size musics)
3.1.1: set a date a few days before today in config:dateafter (format yyyymmdd), and run thecommand 'aytdl update <youtube-channel-not-used-yet>'. Do you only download the most recent videos?
3.1.2: do the force flag allows you to re-download the sames musics again?
3.1.3: do 'aytdl update' works (update all the new musics from added urls)

3.1.4: (unix only for now) do aytdl update -p catch & download the url of the video currectly playing in google-chrome?
3.1.5: are the correct thumbnails correctly embedded in the music file (if the option is set)

3.1.6: do 3.0.0, 3.1.5 and 3.1.0 still work if setting the format 'mp3' instead of 'best' in config:audio-format ?

## upgrading & repair
4.0 : set config:version to 0.0.0 and run any aytdl command. Does it display a warning and stop? Afterwards, does config:version display the latest version?
4.1 : change your config:library\_path, set audio-format to mp3 and set version to 0.0.0, run any aytdl command? Does it display a warning? Is config:library\_path correctly kept? Is audio-format restored to 'best'?
4.2 : during a 'aytdl update <multiple-urls>' command, Ctrl-C interrupt the program. Does the config:clean\_exit is set to false?


If all the above is answered on the positive, autoytdl is good to go!
