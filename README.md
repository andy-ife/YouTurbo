YouTurbo: A lightweight python GUI script for downloading video, audio and playlists from
YouTube and all of the other 1000+ sites supported by yt-dlp. See the full list of supported sites [here](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

# Description
YouTurbo is essentially a GUI wrapper around yt-dlp. **ffmpeg and ffprobe are strongly recommended**.
You can find more information about yt-dlp and its features [here](https://github.com/yt-dlp/yt-dlp).

# Features
- Download audio, video, both or full playlists from several video/audio hosting platforms. All you
  need is a url.
- Customize your download with options like resolution, file format, subtitles and more.
- See your download progress and be alerted when downloads are complete.

# Installation

##  Build from source
For now the only way to install yt-dlp is to build from the source code. Release binaries will be added soon.

1. Clone the repository.
2. **Optional but strongly recommended:** Download ffmpeg and ffprobe for your operating system 
  [here](https://www.ffmpeg.org/). Copy the files to the **bin** directory of this project **OR** install them system-wide.
3. Install the yt-dlp python module. `pip install -r requirements.txt`
4. In the **src** folder, run **main.py**.

# Usage
Usage should be (hopefully) intuitive with the Tkinter GUI.

