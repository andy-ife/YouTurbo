import os
import yt_dlp
import threading
import time

PROJECT_DIR = os.path.dirname(__file__).rsplit('src', 1)[0]  # path to project directory
BIN_DIR = os.path.join(PROJECT_DIR, 'bin')  # path to bin/


def download_video(url, download_dir, file_type, with_subs, on_progress_hook, on_success, on_error):
    def worker():
        if file_type == 'audio only':
            fformat = 'bestaudio'
        elif file_type == 'video only':
            fformat = 'bestvideo'
        else:
            fformat = 'bestvideo+bestaudio'

        options = {
            'format': fformat,
            'writesubtitles': with_subs,
            'progress_hooks': [on_progress_hook],
            'ffmpeg_location': BIN_DIR,
            'no_color': True,
            'subtitleslangs': ['en'],
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }

        yt = yt_dlp.YoutubeDL(options)
        os.chdir(download_dir)

        try:
            yt.download([url])
            time.sleep(0.5)
            on_success()
        except Exception:
            on_error()

    thread = threading.Thread(target=worker)
    thread.start()


def extract_video_info(url, filetype, on_success, on_loading, on_error):  # get video title and best resolution
    on_loading()

    def worker():
        yt = yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio', 'playlist_items': '1'})
        ptxt = ''
        try:
            info_dict = yt.extract_info(url, download=False)

            if 'playlist' in url:  # checking for playlist
                ptxt = '(Full Playlist)'
                formats = info_dict['entries'][0].get('formats')
            else:
                formats = info_dict.get('formats')
            heights = set()
            for f in formats:
                if 'height' in f:
                    if type(f['height']) is int:
                        heights.add(f['height'])

            resolution = max(heights)
            title = info_dict.get('title')

            if filetype == 'audio only':
                result = {'title': f'[AUDIO] {title} {ptxt}', 'resolution': 'Audio only (MP3)'}
            elif filetype == 'video only':
                result = {'title': f'[VIDEO (NO SOUND)] {title} {ptxt}', 'resolution': f'{resolution}p Video (No sound)'}
            else:
                result = {'title': f'[VIDEO] {title} {ptxt}', 'resolution': f'{resolution}p'}

            print(result)
            on_success(result)

        except Exception as e:
            print(e)
            on_error()

    thread = threading.Thread(target=worker)
    thread.start()
