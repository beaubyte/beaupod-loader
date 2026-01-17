# beaupod-loader

A script I made to get top songs from my Last.FM or from YouTube Music playlists/radios, attach metadata, and then download via yt-dlp to an .M4A file for loading onto my iPod.

### Dependancies

- `python3.10` or later
- `python3-pip`
- `ffmpeg` compiled with support for `libfdk_aac`
  - a script is provided to compile a limited version of ffmpeg that supports this codec.

### Instructions

1. `git clone` the repository
2. run `python3 -m venv pyenv` to create a virtual python environment
3. activate the environment with `source pyenv/bin/activate`
4. install dependancies with `pip install -r requirements.txt`
