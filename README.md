# auto-ytdl

I KNOW, YET ANOTHER YOUTUBE-DL WRAPPER. But this one does something others don't: ability to automate your new music downloads, just like package managers automate your updates

# Why does it exist?

[DISCLAIMER: unformal language]

Y'all know how we live in the 5G era, so for music folks that would mean streaming music 24/7... but (one or more of):

- there is no mobile network / wifi at your office / parent's home / hotel room / on the road / at the back of your house
- you have a limited data allowance anyway
- spotify feels like both an ad gatling gun and a noisy radio (because of the network bandwith playing yo-yo)
- your entry-level phone/PC 2.4GHz antenna can't deal with both Wi-Fi music streaming and bluetooth connection to headphone/speakers
- youtube/yt music either replay the same 5 songs forever or goes its way on some crappy music that's unlike everything you like. It's a nice tool to discover new things, but not to actually listen to music
- yeah, music streaming is pretty not here yet

# Who it is for? (at least me, I guess I'm not alone so that's the 'why' part 2)

[DISCLAIMER: personal opinion]

For people who truly enjoy music, nothing beats yet having a local library, even with the hassle of managing, de-duplicating, and updating it constantly. If you

Auto-ytdl is there to help with all that: there are tons of great artists that publish new songs everyday; having a local music library should not mean that we have to forsake listening to those!

# Doesn't it exist already?

No.

The closest I could find is MediaHuman (paid, expensive, closed-source) Youtube-Downloader: as of writing, it seems to have 'tracking' capabilities, and little explications given.
All this looked a bit fishy, it has a nice GUI though.

Moreover, it only offers a .deb package for "GNU/Linux" and .deb support for Arch (btw I use Arch) is not first-class.

# Dependencies

- youtube-dl
- ffmpeg
- python3-pip

# Install

- auto-ytdl will be available in the AUR
  [link placeholder]
- install from source:

```
git clone https://github.com/michaelb/auto-ytdl
cd auto-ytdl
pip install --user .
```

#Usage

Once installed you can run

```
aytdl [COMMAND][OPTIONS] [URLs ..]
```

#Examples
