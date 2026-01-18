# beaupod-loader

A script I made to get top songs from my Last.FM or from YouTube Music playlists/radios, attach metadata, and then download via yt-dlp to an .M4A file for loading onto my iPod. At the current moment, a .env file must be provided with a **API_KEY** (for Last.FM) and a **USERNAME** value.

### Dependancies

- `python3.10` or later
- `python3-pip`
- `python3.10-venv` or later
- `ffmpeg` compiled with support for `libfdk_aac`
  - a bash script is provided to compile a limited version of ffmpeg that supports this codec.
  - to compile ffmpeg with the script, ensure the following dependancies are installed: `bzip2 gcc cmake wget build-essential automake autoconf meson ninja-build pkg-config texinfo zlib1-dev libtool nasm libfdk-aac-dev`

### Instructions

1. `git clone` the repository
2. run `python3 -m venv pyenv` to create a virtual python environment
3. activate the environment with `source pyenv/bin/activate`
4. install python dependancies with `pip install -r requirements.txt`
