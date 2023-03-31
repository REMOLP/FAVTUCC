### IMPORTANT ###
"""
Some things actually does not work because they weren't implemented properly or I was just too lazy to fix some issues.
Mainly the paramaters -D and -d does not work at all. Please do not use them unless you fixed them yourself. In that case, congrats :D

Oh, and also, I know I know, a lot of things are very messy and undocumented but to be honest with you, it was supposed to be just a simple project to
spend some time on something else rather than play games all the time or other procrastinating bs.

Have fun, mate ;D
"""

from favtucc import *
import sys
import os
from random import randint

### User defined vars - START ###
chosenChannel = 1

splicingAlgo = "default"

finalOutputVideoName = channelsMetadata[chosenChannel]["vidOut"] + str(current_vid_num()) + ".mp4"
### User defined vars -   END ###

### Algos impl - START ###

def LILO_ALGO(i_loop, loopIters, iFileDur):
    # Linear in, linear out.
    # As in the name. It splits video in a linear fashion and then concats it in linear fashion again.
    # Invidual sections and parts based on it are of course random, but the rest is linear :)
    
    localOffset = DEF_START + randint(int((iFileDur / loopIters) / 2 - loopIters), int((iFileDur / loopIters)))
    newTS = (iFileDur / loopIters) * (i_loop)+1 + localOffset

    return newTS

### Algos impl -   END ###


def checkArgs():
    global chosenChannel
    global finalOutputVideoName
    global splicingAlgo

    takenArgs = sys.argv

    if len(takenArgs) <= 1:
        print("FAVTUCC aka stupid and completely random clipping program made because of boredom.\n")
        print("Possible arguments:")
        print("\t-D    [EXPERIMENTAL] uses parse_and_check_new_yt_vid function to check for a new video and download it automatically from a specified channel")
        print("\t-d    download a YT video without writing that long-ass command :)")
        print("\t-c    choose a channel from channels.json file (zero-based index)\n")

        print("-c argument is required.")
        sys.exit(0)

    #print(takenArgs[1])
    if takenArgs[1] == "-c":
        chosenChannel = int(takenArgs[2])
        finalOutputVideoName = channelsMetadata[chosenChannel]["vidOut"] + str(current_vid_num()) + ".mp4"
    elif takenArgs[1] == "-D":
        chosenChannel = int(takenArgs[2])
        parse_and_check_new_yt_vid(chosenChannel)
    elif takenArgs[1] == "-d":
        if os.path.isfile("orginput.mp4") == True:
            os.remove("orginput.mp4")

        ytDlCommand = "yt-dlp -f \'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4\' -o \'orginput.%(ext)s\' "+str(takenArgs[2])
        print(ytDlCommand)
        run_command(ytDlCommand)
    else:
        print("I don't undertand you, mate.")
        sys.exit(0)

    # Algorithm to choose by a user
    if len(takenArgs) < 4 or takenArgs[3] == "":
        splicingAlgo = "DEBUGMODE"
    else:
        splicingAlgo = str(takenArgs[3])



### Pre-init or smth. ###
checkArgs()

### Here it really starts ###
if __name__ == "__main__":
    outFiles = []
    txtFileOut = ""

    inputFileDuration = get_duration("orginput.mp4")
    inputFileDuration = int(inputFileDuration) - END_POSTFIX

    # Here specified algo based on user decison starts. It would be better to make it into another func, but for now it is how it is.
    if splicingAlgo == "default":
        #from time import sleep

        for i in range(randint(5, 10)):
            currentTS = randint(DEF_START, inputFileDuration)
            currentSectionDuration = randint(6, 10)
        
            outFileName = TEMPVIDS_FOLDER + "vidsection" + str(i+1) + ".mp4"
            outFiles.append(outFileName)
            run_command('ffmpeg -ss {} -i ./orginput.mp4 -t {} -c:v copy -c:a aac ./{}'.format(seconds_to_timestamp(currentTS), currentSectionDuration, outFileName))

            txtFileOut += "file '"+outFileName+"'\n"
            #sleep(2)

        write_outfiles_to_txt(txtFileOut)
        #run_command('ffmpeg -i concat:"{}|{}|{}|{}|{}" -c:v copy -c:a aac ./outsakaput.mp4'.format(outFiles[0], outFiles[1], outFiles[2], outFiles[3], outFiles[4]))
        run_command('ffmpeg -f concat -safe 0 -i ./filestomerge.txt -c:v libx264 -c:a aac {}'.format(finalOutputVideoName))

        clean_files(outFiles)
        ow_current_vid_num(CURRENT_VIDEO_NUMBER+1)
    elif splicingAlgo == "lilo":
        ### LILO = Linear in, linear out ###
        DEF_START = int(input("Input new video start position for lilo algo. It is important (in seconds): "))
        howMany = randint(5, 10)
        for i in range(howMany):
            currentTS = LILO_ALGO(i, howMany, inputFileDuration)
            currentSectionDuration = randint(6, 10)
        
            outFileName = TEMPVIDS_FOLDER + "vidsection" + str(i+1) + ".mp4"
            outFiles.append(outFileName)
            run_command('ffmpeg -ss {} -i ./orginput.mp4 -t {} -c:v copy -c:a aac ./{}'.format(seconds_to_timestamp(currentTS), currentSectionDuration, outFileName))

            txtFileOut += "file '"+outFileName+"'\n"
            #sleep(2)

        write_outfiles_to_txt(txtFileOut)
        #run_command('ffmpeg -i concat:"{}|{}|{}|{}|{}" -c:v copy -c:a aac ./outsakaput.mp4'.format(outFiles[0], outFiles[1], outFiles[2], outFiles[3], outFiles[4]))
        run_command('ffmpeg -f concat -safe 0 -i ./filestomerge.txt -c:v libx264 -c:a aac {}'.format(finalOutputVideoName))

        clean_files(outFiles)
        ow_current_vid_num(CURRENT_VIDEO_NUMBER+1)
    else:
        print(splicingAlgo)
        print("Not implemented yet!")

print("DONE!")
