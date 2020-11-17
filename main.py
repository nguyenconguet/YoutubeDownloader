from tkinter import *
from pytube import YouTube

# yt = YouTube("https://www.youtube.com/watch?v=3KadWjpqDXs&ab_channel=HoaproxOfficial")

# ls = yt.streams.filter(subtype='mp4').order_by('resolution').desc().all()

# for i in ls:
#     print(i)
# ls[0].download()

root = Tk()
root.title("Download videos, audio from Youtube")
root.geometry('500x300')

title = Label(root, text = "YouTube Downloader", font=('System Bold', 20))
# label.place(y = 30)
title.pack(pady=20)
ls_stream = []
def get_link():
    url = str(url_link.get())
    yt = YouTube(url)
    global ls_stream
    ls_stream = yt.streams.filter(subtype='mp4').order_by('resolution').desc().all()
    for i in ls_stream:
        listBox.insert(END, i)


def download():
    stream = listBox.curselection()
    index = stream[0]
    print(ls_stream[index])
    ls_stream[index].download()

label = Label(root, text = "Paste link address", font=('System Bold', 15))
label.pack()

url = StringVar()
url_link = Entry(root, width=40, textvariable = url, font=('System', 12))
url_link.pack(pady=10, ipady=2)

btn_getLink = Button(root, text="Get Link", command=get_link)
btn_getLink.place(x = 80, y = 170)

btn_download = Button(root, text="Download", command=download)
btn_download.place(x = 80, y = 220)

listBox = Listbox(root, bg='white', width=30)
listBox.place(x = 240, y=150)

# scrollbarx = Scrollbar(root, orient="vertical")
# scrollbarx.config(command=listBox.yview)
# scrollbarx.pack(side="right", fill="y")

# scrollbarx = Scrollbar(root, orient="horizontal")
# scrollbarx.config(command=listBox.xview)
# scrollbarx.pack(side="bottom", fill="x")

root.mainloop()