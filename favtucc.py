"""
The command to download videos ==> yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o 'orginput.%(ext)s' [LINK]
"""

import datetime
import subprocess
import sys
import os

import json

# Open the JSON file in read mode
with open('channels.json', 'r', encoding="utf-8") as f:
    # Load the contents of the file into a Python object
    jsonData = json.load(f)


channelsMetadata = jsonData["fullArray"]


def seconds_to_timestamp(seconds):
    return str(datetime.timedelta(seconds=seconds))

def get_duration(input_video):
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(input_video)
    output = subprocess.check_output(cmd, shell=True)
    return float(output)

def run_command(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]

def write_outfiles_to_txt(txtmsg):
    txt = open("./filestomerge.txt", "w", encoding="utf-8")
    txt.write(txtmsg)
    txt.close()

def clean_files(filesArr):
    import os

    for i in range(len(filesArr)):
        os.remove(filesArr[i])

    print("WYCZYSZCZONO FOLDER 'tempvids'!")

def current_vid_num():
    currentVidNum = -1

    fileWithStoredNum = open("./__new.txt", "r")
    currLine = fileWithStoredNum.readline().strip()
    # print(int(currLines))
    currentVidNum = int(currLine)
    fileWithStoredNum.close()

    return currentVidNum


def ow_current_vid_num(currentNewNum):
    fileWithStoredNum = open("./__new.txt", "w")
    fileWithStoredNum.write(str(currentNewNum))
    fileWithStoredNum.close()

def current_yt_vid():
    currentVid = ""

    fileWithStoredNum = open("./__nvut.txt", "r")
    currLine = fileWithStoredNum.readline().strip()
    currentVidId = str(currLine)

    currLine = fileWithStoredNum.readline().strip()
    currentVidDate = str(currLine)
    
    fileWithStoredNum.close()

    return [currentVidId, currentVidDate]

def ow_current_yt_vid(currentNewId, currentNewDate):
    print("NADPISUJE DANE W PLIKU '__nvut.txt'!")
    fileWithStoredNum = open("./__nvut.txt", "w", encoding="utf-8")
    fileWithStoredNum.write(str(currentNewId)+"\n")
    fileWithStoredNum.write(str(currentNewDate))
    fileWithStoredNum.close()

    
def parse_and_check_new_yt_vid(chosenChannel):
    import feedparser
    
    ytChannel = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id={}".format(channelsMetadata[chosenChannel]["channelID"])) 
    newestVideoId = ytChannel.entries[0].yt_videoid
    print(newestVideoId)
    newestVideoDate = ytChannel.entries[0].published
    print(newestVideoDate)

    funcReturnedId, funcReturnedDate = current_yt_vid()

    if (funcReturnedId != newestVideoId) and (funcReturnedDate != newestVideoDate):
        vLINK = "https://www.youtube.com/watch?v="+newestVideoId
        os.remove("orginput.mp4")
        run_command("yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o 'orginput.%(ext)s' {}".format(vLINK))

        ow_current_yt_vid(newestVideoId, newestVideoDate)
    else:
        print("Video is already up to date!")
        sys.exit(0)

    return [newestVideoId, newestVideoDate]



# CONST
DEF_START = 120 # seconds
END_POSTFIX = 40 # seconds
TEMPVIDS_FOLDER = "./tempvids/"
CURRENT_VIDEO_NUMBER = current_vid_num()
