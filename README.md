# Project Title
YouTurbo: A lightweight python GUI (Tkinter) script for downloading video, audio and playlists from
YouTube, Twitch, 4tube and a multitude of other video and audio hosting platforms. Supports Windows only.

# Description
YouTurbo is essentially a GUI wrapper around yt-dlp. **ffmpeg and ffprobe are strongly recommended**.
You can find more information about yt-dlp and its features [here](https://github.com/yt-dlp/yt-dlp).

# Features
- Download audio, video, both or full playlists from several video/audio hosting platforms. All you
  need is a url.
- Customize your download with options like resolution, file format, subtitles and more.
- See your download progress and be alerted when downloads are complete.

# Installation

1. Clone the repository.
2. **Optional but strongly recommended:** Download ffmpeg and ffprobe [here](https://www.ffmpeg.org/).
   Copy the .exe files to the **bin** directory of this project **OR** install them system-wide.
3. Install the yt-dlp python module. `pip install -r requirements.txt`
4. In the **src** folder, run **main.py**.

# Usage
Usage should be (hopefully) intuitive with the Tkinter GUI.

