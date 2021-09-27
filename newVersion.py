from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import os

BG_COLOR = ""


# create init tkinter
root = Tk()
root.title('Youtube Downloader - NDC')
root.geometry('800x400')

previousprogress = 0


class YoutubeDownloader:
    def __init__(self, main):
        self.ls_yt_streams = None
        self.ls_streams_view = None
        self.map_view_items = dict()
        self.path_folder = os.getcwd()

        # main frame
        self.main = main
        self.topFrame = Frame(main, bg="yellow")
        self.bottomFrame = Frame(main, bg="black")
        self.leftFrame = Frame(
            self.bottomFrame, bg="#ffff99")
        self.rightFrame = Frame(
            self.bottomFrame, bg="blue")

        # add main frame to main grid
        self.main.rowconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=2)
        self.main.columnconfigure(0, weight=1)

        self.topFrame.grid(row=0, sticky="nsew")
        self.bottomFrame.grid(row=1, sticky="nsew")

        self.bottomFrame.rowconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.leftFrame.grid(row=0, column=0, sticky="nsew")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")

        # top Frame
        self.topFrame.rowconfigure(0, weight=1)
        self.topFrame.rowconfigure(1, weight=4)
        self.topFrame.columnconfigure(0, weight=1)

        # title
        self.title = Label(
            self.topFrame, text="Youtube Downloader - NDC", font=('System Bold', 20), bg="yellow")
        self.title.grid(row=0, column=0)

        self.inputFrame = Frame(self.topFrame)
        self.inputFrame.grid(row=1)
        self.inputFrame.rowconfigure(0, weight=1)
        self.inputFrame.columnconfigure(0, weight=3)
        self.inputFrame.columnconfigure(1, weight=1)

        # input
        self.inputLink = Entry(self.inputFrame, width=50,
                               textvariable=StringVar(), font=('Andale Mono', 14, 'normal'))
        self.inputLink.grid(row=0, column=0)

        # submit btn
        self.getBtn = Button(
            self.inputFrame, text="Get Link", font=('Andale Mono', 12), command=self.get_link)
        self.getBtn.grid(row=0, column=1)

        # bottom frame
        # left frame
        self.leftFrame.rowconfigure(0, weight=1)
        self.leftFrame.rowconfigure(1, weight=1)
        self.leftFrame.columnconfigure(0, weight=1)
        self.youtubeTitle = Label(
            self.leftFrame, wraplength=250, justify=CENTER, text="Title of video", font=('Andale Mono', 12), bg="#ffff99")
        self.youtubeTitle.grid(row=0, column=0, sticky='nesw')

        self.selectPathBtn = Button(
            self.leftFrame, text="Select Save Folder", font=('Andale Mono', 12), bg="#cc9900", command=self.get_save_folder)
        self.selectPathBtn.grid(
            row=1, column=0, sticky='ew')

        # right frame
        self.rightFrame.rowconfigure(0, weight=1)
        self.rightFrame.rowconfigure(1, weight=3)
        self.rightFrame.columnconfigure(0, weight=1)

        self.filterFrame = Frame(self.rightFrame)
        self.filterFrame.grid(row=0, column=0, sticky='nesw')
        self.filterFrame.rowconfigure(0, weight=1)
        self.filterFrame.columnconfigure(0, weight=1)
        self.filterFrame.columnconfigure(1, weight=1)
        self.filterFrame.columnconfigure(2, weight=1)
        self.filterFrame.columnconfigure(3, weight=1)

        self.radioOption = StringVar()
        self.video_audio_filter = Radiobutton(
            self.filterFrame, text="Video & Audio", font=('Andale Mono', 12), bg="#6699ff", variable=self.radioOption, value="VideoAudio")
        self.video_audio_filter.grid(row=0, column=0, sticky='news')

        self.video_filter = Radiobutton(
            self.filterFrame, text="Video", font=('Andale Mono', 12), bg="#6699ff", variable=self.radioOption, value="Video")
        self.video_filter.grid(row=0, column=1, sticky='news')

        self.audio_filter = Radiobutton(
            self.filterFrame, text="Audio", font=('Andale Mono', 12), bg="#6699ff", variable=self.radioOption, value="Audio")
        self.audio_filter.grid(row=0, column=2, sticky='news')

        self.filterBtn = Button(
            self.filterFrame, text="Filter", font=('Andale Mono', 12), bg="#6699ff", command=self.get_filter)
        self.filterBtn.grid(row=0, column=3, sticky='news')

        self.rightBottomFrame = Frame(self.rightFrame, bg="red")
        self.rightBottomFrame.grid(row=1, column=0, sticky='news')
        self.rightBottomFrame.columnconfigure(0, weight=3)
        self.rightBottomFrame.columnconfigure(1, weight=1)
        self.rightBottomFrame.rowconfigure(0, weight=1)

        # list view
        self.listBox = Listbox(self.rightBottomFrame, font=(
            'Andale Mono', 12), bg="#ccff99")
        self.listBox.grid(row=0, column=0, sticky='nsew')

        self.downloadBtn = Button(
            self.rightBottomFrame, text='Download', font=('Andale Mono', 12), command=self.download)
        self.downloadBtn.grid(row=0, column=1, sticky='ew')

    def get_link(self):
        url = str(self.inputLink.get())
        yt = YouTube(url)
        yt.register_on_progress_callback(self.on_progress)

        print(yt.title)
        self.youtubeTitle.config(text=yt.title)

        self.ls_yt_streams = yt.streams
        # print(self.ls_yt_streams)
        # show to listBox
        self.listBox.delete(0, END)
        self.map_view_items.clear()
        for i in self.ls_yt_streams:
            if i.type == 'audio':
                mime_type, abr, size = self.get_item_feature(i)
                item = str(mime_type) + ", " + str(abr) + \
                    ", " + str(size) + "MB"
            else:
                mime_type, res, fps, size = self.get_item_feature(i)
                item = str(mime_type) + ", " + str(res) + \
                    ", " + str(fps) + "fps" + ", " + str(size) + "MB"
            self.map_view_items[item] = i
            self.listBox.insert(END, item)

    def get_item_feature(self, item):
        if item.type == 'audio':
            mime_type = item.mime_type
            abr = item.abr
            size = round(item.filesize / 1048576, 2)
            return mime_type, abr, size
        else:
            mime_type = item.mime_type
            res = item.resolution
            fps = item.fps
            size = round(item.filesize / 1048576, 2)
            return mime_type, res, fps, size

    def get_filter(self):
        filterMethod = self.radioOption.get()
        if filterMethod == "VideoAudio":
            self.ls_streams_view = self.ls_yt_streams.filter(
                progressive=True).order_by('resolution').desc()
            # print(self.ls_streams_view)

            self.listBox.delete(0, END)
            # self.map_view_items.clear()
            for i in self.ls_streams_view:
                mime_type, res, fps, size = self.get_item_feature(i)
                item = str(mime_type) + ", " + str(res) + \
                    ", " + str(fps) + "fps" + ", " + str(size) + "MB"
                self.map_view_items[item] = i
                self.listBox.insert(END, item)
        elif filterMethod == "Video":
            self.ls_streams_view = self.ls_yt_streams.filter(
                progressive=False, type='video').order_by('resolution').desc()
            # print(self.ls_streams_view)

            self.listBox.delete(0, END)
            # self.map_view_items.clear()
            for i in self.ls_streams_view:
                mime_type, res, fps, size = self.get_item_feature(i)
                item = str(mime_type) + ", " + str(res) + \
                    ", " + str(fps) + "fps" + ", " + str(size) + "MB"
                self.map_view_items[item] = i
                self.listBox.insert(END, item)
        elif filterMethod == 'Audio':
            self.ls_streams_view = self.ls_yt_streams.filter(
                progressive=False, type='audio').order_by('abr').desc()
            # print(self.ls_streams_view)

            self.listBox.delete(0, END)
            # self.map_view_items.clear()
            for i in self.ls_streams_view:
                mime_type, abr, size = self.get_item_feature(i)
                item = str(mime_type) + ", " + str(abr) + \
                    ", " + str(size) + "MB"
                self.map_view_items[item] = i
                self.listBox.insert(END, item)

    def get_save_folder(self):
        self.path_folder = filedialog.askdirectory()

    def on_progress(self, stream, chunk, bytes_remaining):
        self.downloadBtn.configure(text="Downloading...", state=DISABLED)
        # print("downloading..")
        filesize = round(stream.filesize / (1024 * 1024), 2)

        download_size = round(
            (stream.filesize - bytes_remaining) / (1024 * 1024), 2)

        print('DOWNLOADING: ' + str(download_size) +
              "MB/" + str(filesize) + "MB")

    def download(self):
        item = self.listBox.get(self.listBox.curselection())
        stream = self.map_view_items[item]
        stream.download(self.path_folder)
        self.downloadBtn.configure(text="Download", state=NORMAL)
        print("Complete")


a = YoutubeDownloader(root)

root.mainloop()
