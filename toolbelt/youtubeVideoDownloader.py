from pytube import YouTube
import tkinter as tk
import os

RESOLUTIONOPTIONS = [
    "144p",
    "240p",
    "360p",
    "480p",
    "720p",
    "1080p"
]

fileExtensionType = "mp4"
audioOnly = False

def setFileExtensionTypeMP3():
    global audioOnly
    audioOnly = True
def setFileExtensionTypeMP4():
    global audioOnly
    audioOnly = False

def getYoutubeVideo():
    youtubeVideoData = YouTube(urlTextBox.get())
    if audioOnly:
        stream = youtubeVideoData.streams.filter(file_extension="mp4", only_audio=audioOnly).first()
    else:
        stream = youtubeVideoData.streams.filter(file_extension="mp4", progressive=True, resolution="720p").first()
        
    MP4path = stream.download()
    base, ext = os.path.splitext(MP4path)
    MP3path = base + ".mp3"
    os.rename(MP4path, MP3path)
    


APP = tk.Tk()

title = tk.Label(APP, text="Youtube To MP3/MP4 converter")
title.grid(column=0, row=0, columnspan=3)

MP3button = tk.Button(APP, text="MP3", command=setFileExtensionTypeMP3)
MP4button = tk.Button(APP, text="MP4", command=setFileExtensionTypeMP4)

MP3button.grid(column=0, row=3)
MP4button.grid(column=2, row=3)

urlTextBox = tk.Entry(APP)
urlTextBox.grid(column=0, row=2, columnspan=3)


variable=tk.StringVar(APP)
variable.set(RESOLUTIONOPTIONS[4])

resolutionMenu = tk.OptionMenu(APP, variable, *RESOLUTIONOPTIONS)
resolutionMenu.grid(column=1, row=4)

checkButton = tk.Button(APP, text="check")
checkButton.grid(column=0, row=5)

searchButton = tk.Button(APP, text="search", command=getYoutubeVideo)
searchButton.grid(column=2, row=5)

ytDataVideo = tk.Label(APP, text="")
ytDataAuthor = tk.Label(APP, text="")
ytDataLength = tk.Label(APP, text="")


APP.mainloop()



