# Main Ui Class
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_logic as ytl
import os
from res import colors

# Icons
APP_ICON = os.path.join(ytl.PROJECT_DIR, 'src', 'res', 'icons', 'app_icon.png')
CHKBOX_ICON = os.path.join(ytl.PROJECT_DIR, 'src', 'res', 'icons', 'chkbox_icon.png')
CARET_ICON = os.path.join(ytl.PROJECT_DIR, 'src', 'res', 'icons', 'caret_icon.png')

DEFAULT_TEXT = 'Paste your video or playlist link here'

DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')

class MainApplication:
    def __init__(self):
        # Root window
        self.root = tk.Tk()
        self.root.geometry('700x420')
        self.root.iconphoto(False, tk.PhotoImage(file=APP_ICON))
        self.root.title('YouTurbo: Youtube Video Downloader')
        # self.root.resizable(False, False)

        self.searchquery = tk.StringVar(self.root)  # ------Video url string-------#
        self.has_extracted_vid_info = False
        self.has_shown_dl_info_on_grid = False
        self.is_loading = False # Nifty variable that checks if we are currently on in an operation. prevents spam

        # Search bar frame (takes the border attributes, simulates padding)
        self.sframe = tk.Frame(
            self.root,
            highlightthickness=2,
            highlightbackground=colors.red_orange_dark,
            highlightcolor=colors.red_orange_medium,
        )
        self.sframe.columnconfigure(1, weight=1)  # widgets in col 2 should fill available x space
        self.sframe.pack(pady=(24, 16), padx=20, fill='x')

        # Search bar (the actual search bar within sframe)
        self.searchbar = tk.Entry(
            self.sframe,
            relief=tk.FLAT,
            textvariable=self.searchquery,
            font=('Corbel', 12),
            fg=colors.grey_light,
            borderwidth=12  # increasing invisible border's width creates padding
        )
        self.searchbar.insert(tk.END, DEFAULT_TEXT)
        self.searchbar.bind('<Button-1>', self.clear_searchbar)
        self.searchbar.bind('<Return>', self.on_download_btn_click)
        self.searchbar.bind('<Control-v>', self.delayed_extract_vid_info)
        self.searchbar.grid(row=0, columnspan=2, sticky=tk.W+tk.E)

        # Url checkbox icon label
        # to be added to ui when available formats are fetched successfully (valid yt url)
        # grid params: row=0, column=1, sticky=tk.E, padx=(0, 20)
        img = tk.PhotoImage(file=CHKBOX_ICON, master=self.sframe)
        self.chkbox_icon = tk.Label(
            self.sframe,
            anchor=tk.CENTER,
            image=img,
            height=20,
            width=20
        )

        # Window body frame
        self.bframe = tk.Frame(self.root)
        self.bframe.columnconfigure(3, weight=1)  # widgets in col 3 should fill available x space
        self.bframe.pack(fill='x', padx=20, )

        # File type label
        self.ftlabel = tk.Label(
            self.bframe,
            text='File type',
            font=('Corbel', 11)
        )
        self.ftlabel.grid(row=0, column=0, sticky=tk.W)

        # File type radio buttons
        self.filetype = tk.StringVar(self.bframe, 'both')  # ----------File type string----------#
        self.aud_radiobutton = tk.Radiobutton(
            self.bframe,
            text='Audio only',
            variable=self.filetype,
            font=('Corbel', 11),
            value='audio only',
            selectcolor=colors.red_orange_extra_light,
            command=self.delayed_extract_vid_info
        )
        self.aud_radiobutton.grid(row=1, column=0, padx=(0, 24))

        self.vid_radiobutton = tk.Radiobutton(
            self.bframe,
            text='Video only',
            variable=self.filetype,
            font=('Corbel', 11),
            value='video only',
            selectcolor=colors.red_orange_extra_light,
            command=self.delayed_extract_vid_info
        )
        self.vid_radiobutton.grid(row=1, column=1, padx=(0, 24))

        self.both_radiobutton = tk.Radiobutton(
            self.bframe,
            text='Both (Default)',
            variable=self.filetype,
            font=('Corbel', 11),
            value='both',
            selectcolor=colors.red_orange_extra_light,
            command=self.delayed_extract_vid_info
        )
        self.both_radiobutton.grid(row=1, column=2, padx=(0, 24))

        # Subtitles checkbox
        self.has_subtitles = tk.BooleanVar(self.bframe, False)  # ---------Subtitles boolean----------#
        self.subs_checkbox = tk.Checkbutton(
            self.bframe,
            text='Subtitles',
            font=('Corbel', 11),
            offvalue=False,
            onvalue=True,
            variable=self.has_subtitles,
        )
        self.subs_checkbox.grid(row=1, column=3, sticky=tk.E)

        # Horizontal line separator using Frame
        self.separator1 = tk.Frame(self.bframe, height=1, background=colors.grey_extra_light)
        self.separator1.grid(row=2, columnspan=4, pady=10, sticky=tk.W + tk.E)

        # Download location label
        self.dllabel = tk.Label(
            self.bframe,
            text='Choose download location',
            font=('Corbel', 11)
        )
        self.dllabel.grid(row=3, columnspan=2, sticky=tk.W)

        # --------Path to download directory as string---------#
        self.download_dir = tk.StringVar(self.bframe, DEFAULT_DOWNLOAD_DIR)
        # Download location button
        self.download_dir_btn = tk.Button(
            self.bframe,
            textvariable=self.download_dir,
            font=('Corbel', 11,),
            anchor=tk.W,
            relief=tk.FLAT,
            bg=colors.grey_ultra_light,
            padx=8,
            activebackground=colors.grey_extra_light,
            command=self.select_download_dir
        )
        self.download_dir_btn.grid(row=4, columnspan=4, sticky=tk.W + tk.E, pady=(0, 30))

        # Download information labels
        # dl_infolabel will be added to grid when ytl.download or ytl.extract_info is called
        # grid params: self.dl_infolabel.grid(row=5, columnspan=2, sticky=tk.W)
        self.dl_infotext = tk.StringVar(self.bframe, 'Downloading...')  # -------Download info text--------#
        self.dl_infolabel = tk.Label(
            self.bframe,
            textvariable=self.dl_infotext,
            font=('Cordana', 11,)
        )

        # dl_progresslabel will be added to grid only when video download starts
        # grid params = self.dl_progresslabel.grid(row=5, column=3, sticky=tk.E)
        self.download_progress = tk.IntVar(self.bframe, 0)  # -------download progress integer-------#
        self.download_progress_text = tk.StringVar(self.bframe, f'{self.download_progress.get()}%')
        self.dl_progresslabel = tk.Label(
            self.bframe,
            textvariable=self.download_progress_text,
            font=('Cordana', 11,)
        )

        # Progressbar. Determinate for ytl.download_video, indeterminate for ytl.extract_info
        self.progressbar = ttk.Progressbar(
            self.bframe,
            mode='determinate',
            orient=tk.HORIZONTAL,
            variable=self.download_progress,
        )
        self.progressbar.grid(row=6, columnspan=4, pady=(0, 20), sticky=tk.W + tk.E)

        # -------------Video title------------------
        # for label: self.video_title_label.grid(row=7, columnspan=4, pady=(0, 20))
        self.video_title = tk.StringVar(self.bframe, 'The Legend of the Green Man')
        self.video_title_label = tk.Label(
            self.bframe,
            textvariable=self.video_title,
            font=('Cordana', 14, 'bold')
        )

        # Bottom frame
        self.footframe = tk.Frame(self.root)
        self.footframe.columnconfigure(0, weight=1)
        self.footframe.columnconfigure(1, weight=1)
        self.footframe.columnconfigure(2, weight=1)
        self.footframe.pack(fill='x', padx=20)

        # Download button
        self.download_btn = tk.Button(
            self.footframe,
            text='Download',
            font=('Corbel', 11, 'bold'),
            padx=110,
            pady=10,
            fg=colors.white,
            bg=colors.space_cadet,
            activeforeground=colors.white,
            activebackground=colors.space_cadet_dark,
            command=self.on_download_btn_click
        )
        self.download_btn.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.resolution_text = tk.StringVar(self.footframe, '1080p Video (Best quality)')  # ------text to display on menu btn-------#
        caret_img = tk.PhotoImage(file=CARET_ICON)

        self.fmenu_button = tk.Menubutton(
            self.footframe,
            highlightcolor=colors.space_cadet,
            highlightthickness=2,
            highlightbackground=colors.space_cadet,
            bg=colors.white,
            activebackground=colors.grey_ultra_light,
            font=('Cordana', 11),
            pady=12,
            takefocus=True,
            textvariable=self.resolution_text,
            image=caret_img,
            compound=tk.RIGHT,
        )

        self.root.mainloop()

    def select_download_dir(self):
        directory = filedialog.askdirectory(title='Choose Download Location')
        if directory:
            self.download_dir.set(directory)

    def on_download_success(self):
        self.is_loading = False
        # Forget download info
        self.has_shown_dl_info_on_grid = False
        self.has_extracted_vid_info = False

        # Clear Loading info
        self.dl_infolabel.grid_forget()
        self.dl_progresslabel.grid_forget()
        self.download_progress_text.set('0%')

        messagebox.showinfo(
            'Download Success',
            f'{self.video_title.get()} was downloaded successfully.'
            f'\n\nLocation: {self.download_dir.get()}'
        )

    def on_download_progress_hook(self, d):
        # update progress bar and label on every progress hook from yt-dlp
        # d represents progress hook object
        if d['status'] == 'downloading':
            speed = d.get('speed')
            if speed:
                speed = round((speed / 1024.0), 1)
            self.dl_infotext.set(f'Downloading... ({speed} KB/s)')
            current_progress = int(float(d['_percent_str'].replace('%', '')))
            if current_progress > self.download_progress.get() and current_progress != 100:
                self.download_progress.set(current_progress)
                self.download_progress_text.set(f'{current_progress}%')
        elif d['status'] == 'finished':
            self.dl_infotext.set('Finishing up...')
            self.download_progress.set(100)
            self.download_progress_text.set(f'100%')

    def on_download_error(self):
        self.is_loading = False
        # Clear Loading information
        self.dl_infolabel.grid_forget()
        self.dl_progresslabel.grid_forget()
        self.download_progress_text.set('0%')

        # Reset loading bar
        self.progressbar.configure(mode='determinate')
        self.download_progress.set(0)

        # Forget download info
        self.has_shown_dl_info_on_grid = False

        messagebox.showerror(
            'Error downloading video',
            'Possible reasons:\n\n- Poor internet connection\n- Video unavailable')

    def on_extract_info_success(self, info_dict):
        self.is_loading = False
        self.has_extracted_vid_info = True
        # Show Checkbox icon
        self.chkbox_icon.grid(row=0, column=1, sticky=tk.E, padx=(0, 20))

        # Show Video title and resolution
        self.video_title.set(info_dict['title'])
        self.resolution_text.set(f"{info_dict['resolution']} (Best quality)")
        self.show_video_info()

        # Clear Loading information
        self.dl_infolabel.grid_forget()

        # Reset loading bar
        self.progressbar.stop()
        self.progressbar.configure(mode='determinate')
        self.download_progress.set(0)

    def on_extract_info_loading(self):
        self.has_extracted_vid_info = False
        # Clear checkbox icon
        self.chkbox_icon.grid_forget()

        # show Loading information
        self.dl_infotext.set('Fetching video information...')
        self.dl_infolabel.grid(row=5, columnspan=2, sticky=tk.W)

        # activate Loading bar
        self.progressbar.configure(mode='indeterminate')
        self.progressbar.start(10)

    def on_extract_info_error(self):
        self.is_loading = False
        self.has_extracted_vid_info = False
        # Clear checkbox icon
        self.chkbox_icon.grid_forget()

        # clear Loading information
        self.dl_infolabel.grid_forget()

        # reset Loading bar
        self.progressbar.stop()
        self.progressbar.configure(mode='determinate')
        self.download_progress.set(0)

        messagebox.showerror(
            'Could not fetch video info',
            'Possible reasons:\n\n- Invalid video url\n- Poor internet connection')

    def show_video_info(self):
        self.footframe.columnconfigure(3, weight=1)
        self.fmenu_button.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.video_title_label.grid(row=7, columnspan=4, pady=(0, 10))

    def hide_video_info(self):
        self.fmenu_button.grid_forget()
        self.footframe.columnconfigure(3, weight=0)
        self.video_title_label.grid_forget()

    def clear_searchbar(self, event=None):
        if self.searchbar.get() == DEFAULT_TEXT:
            self.searchbar.delete(0, tk.END)
            self.searchbar.configure(fg='black')

    def download_video(self, event=None):
        ytl.download_video(
            url=self.searchquery.get().strip(),
            download_dir=self.download_dir.get(),
            file_type=self.filetype.get(),
            with_subs=self.has_subtitles.get(),
            on_progress_hook=self.on_download_progress_hook,
            on_error=self.on_download_error,
            on_success=self.on_download_success
        )

    def on_download_btn_click(self, event=None):
        if self.searchquery.get() != '' and self.searchquery.get() != DEFAULT_TEXT:
            if self.has_extracted_vid_info and not self.is_loading:
                self.is_loading = True
                self.dl_infotext.set('Preparing download...')
                self.dl_infolabel.grid(row=5, columnspan=2, sticky=tk.W)
                self.dl_progresslabel.grid(row=5, column=3, sticky=tk.E)
                self.download_video()
            else:
                self.delayed_extract_vid_info()
        else:
            messagebox.showerror('Missing url', 'Enter a valid video or playlist link')

    def extract_vid_info(self, event=None):
        if self.searchquery.get() != '' and self.searchquery.get() != DEFAULT_TEXT and not self.is_loading:
            self.is_loading = True
            ytl.extract_video_info(
                url=self.searchquery.get().strip(),
                filetype=self.filetype.get(),
                on_success=self.on_extract_info_success,
                on_error=self.on_extract_info_error,
                on_loading=self.on_extract_info_loading
            )

    def delayed_extract_vid_info(self, event=None):
        self.searchbar.after(500, self.extract_vid_info)


MainApplication()
