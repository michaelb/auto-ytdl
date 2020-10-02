# auto-ytdl

![](https://img.shields.io/badge/Release-v1.2.3-green.svg)

I know, _yet another_ youtube-dl wrapper. But this one does something others don't: ability to automate your new music downloads, just like package managers automate your updates.

```
aytdl update
```

And that's it.
(Some initial setup is required of course, so auto-ytdl knows what music to download, but the most used commands are that simple)

## v1.2.3 changelog

> Soundcloud is now explicitly supported, though the user should tweak config options to not be limited to free-tier low quality audio.

> Windows support

> fix music with no length bug

# Table of Contents

- [Why does it exist? / Motivation / Rant](#why-does-it-exist--motivation--rant)
- [Doesn't it exist already?](#doesnt-it-exist-already)
- [How does it works?](#how-does-it-works)
- [Features](#features)
- [Dependencies](#dependencies)
- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)

# Why does it exist? / Motivation / Rant / you can skip this part

[DISCLAIMER: informal language]

Y'all know how we live in the 5G era, so for us music \* folks that would mean streaming music 24/7... but (one or more of):

- there is no mobile network / wifi at your office / parent's home / hotel room / on the road / at the back of your house
- you have a limited data allowance anyway
- spotify feels like both an ad gatling gun and a noisy radio (because of the network bandwith playing yo-yo)
- your entry-level phone/PC 2.4GHz antenna can't deal with both Wi-Fi music streaming and bluetooth connection to headphone/speakers
- youtube/yt music either replay the same 5 songs forever or goes its way on some crappy music that's unlike everything you like. It's a nice tool to discover new things, but not to actually listen to music. Some other services\*\* may be relevant to audiophile-class folks, but down here the _de-facto_ service for music is Youtube.
- yeah, music streaming is pretty not here yet

[DISCLAIMER: personal opinion]

For people who truly enjoy music \*, nothing beats yet having a local library, even with the hassle of managing, de-duplicating, and updating it constantly.

Auto-ytdl is there to help (you) with all that: there are tons of great artists that publish new songs everyday; having a local music library should not mean that we have to forsake listening to those!
Plus, auto-ytdl comes with management of duplicates of newly-downloaded songs, based on metadata so you don't have multiples identical song but from different youtube channels.

\* (_yes_ I know youtube and other video streaming services do not have extremely good audio, but it's out of convenience): hardcore audiophile abstain

# Doesn't it exist already?

No.

However, [olivia](https://github.com/keshavbhatt/olivia) is a music player that propose a similar feature named 'smart playlist', the beta I tested could auto-download individual songs. You may want to check it out!

It's more of an all-rounder and I believe auto-ytdl + your favorite music player may be a better combo _if your use case is similar to mine_.

[deserves mention for existing]

The closest idea I could find is MediaHuman's (paid, expensive, closed-source) Youtube-Downloader: as of writing, it seems to have 'tracking' capabilities, and little explications given.
All this looked a bit fishy, though it has a nice GUI. It also only offers a .deb package for "GNU/Linux OS" and .deb support for Arch (btw I use Arch) is not first-class.

# How does it works?

see also [Usage](#usage) and [Examples](#examples)

1. Add some of your favorite (youtube\*) channels / referencers /artists

2. At your next update command, all newly-released music from specified sources will be downloaded, cleaned, de-duplicated, and added to your music library.

3. [optionnal] Tinker with the options

\* playlist or channels from Dailymotion, vimeo or anything youtube-dl can download from can in theory work, but have not been tested yet

# Features

- Auto-download of all new music from a simple command (music-only download, best quality available (often opus format ~160kbps for youtube), no conversion by default)
- Add/remove/list all your favorite music providers; mainly tested on youtube and soundcloud channels, but should work on playlist, and other video platforms
- Clean tags, so e.g. the displayed artist name does _not_ look like "Nirvana (lyrics) [Music video] official" but just "Nirvana"
- Filter by tags so only 'true' and unique songs (according to config) end up in your library
- Ignore the filter if you really want that weird video
- Can still handle one-shot downloads, or include older songs of (newly discovered) artists
- Comprehensive config options
- No missing/skipping/forgetting songs, even if a previous download was interrupted
- Download video currently playing in chrome/youtube (link that one to a shortcut)
- Thumbnail embedding supported for mp3 and opus (default) format

# Dependencies

- youtube-dl (need to be in the PATH or current folder)
- ffmpeg (need to be in the PATH or current folder)
- pip/python3-pip (need to be in the PATH or current folder)

(optionnal dependency for better OPUS handling, (windows users, don't bother))

- kid3-cli [AUR](https://aur.archlinux.org/packages/kid3-cli/) [website](https://kid3.kde.org/)

Some python modules, such as music-tag and mutagen, will be pulled automatically. If that step fails, you can run `pip install -r dependencies.txt` (or `python3-pip ....`)

# Install

(Install the dependencies first)

- auto-ytdl is available in the AUR
  [here](https://aur.archlinux.org/packages/auto-ytdl-git/)
- install from source:

```
git clone https://github.com/michaelb/auto-ytdl
cd auto-ytdl
pip install --user .

# to uninstall if installed manually
pip uninstall auto-ytdl
```

# Usage

Once installed you can run

```
aytdl [COMMAND][OPTIONS] [URLs ..]
```

# Examples

```
# asking for help
aytdl --help

#asking for help about 'update' command
aytdl update --help


#edit the config file (you should do that, rather sooner than later)
aytdl edit

#add Mr SuicideSheep to followed channels
aytdl add https://www.youtube.com/channel/UC5nc_ZtjKW1htCVZVRxlQAQ

#also work with soundcloud, and probably other video platforms such as dailymotion
aytdl add https://soundcloud.com/nemenmusic

#see all the added sources
aytdl list

> url1
> url2
> ...

#remove Mr SuicideSheep channel from followed sources
aytdl remove https://www.youtube.com/channel/UC5nc_ZtjKW1htCVZVRxlQAQ

#download all new music from all sources
aytdl update


#download rick's astley famous song
aytdl update https://www.youtube.com/watch?v=dQw4w9WgXcQ

#download all music ever from Mr SuicideSheep, no just new ones
aytdl update --include-old https://www.youtube.com/channel/UC5nc_ZtjKW1htCVZVRxlQAQ

# download a 1-hour concerto (not fitting the (configurable) criteria for 'normal' music)
aytdl update https://www.youtube.com/watch?v=PM0HqmptYlY --force

```

### Known Issues & workaround (windows-only)

On Windows, aytdl has trouble with embedding thumbnails with opus and mp3.

MP3 issues with thumbnails migth be bypassed by adding:

embed-thumnail = true

to the end of the config file.
It makes youtube-dl the one in charge of embedding the thumbnail in the mp3, and it should work great!!
