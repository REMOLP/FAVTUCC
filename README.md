# FAVTUCC aka stupid and completely random clipping program made because of boredom.

Just as in the header. This program dates back to February 2022 and now I do not have energy to refactor etc.

Some things actually does not work because they weren't implemented properly or I was just too lazy to fix some issues.
Mainly the paramaters -D and -d does not work at all. Please do not use them unless you fixed them yourself. In that case, congrats :D

Oh, and also, I know I know, a lot of things are very messy and undocumented but to be honest with you, it was supposed to be just a simple project to
spend some time on something else rather than play games all the time or other procrastinating bs.

Have fun, mate ;D

## Prerequisites

You need to have:
- ffmpeg
- Python 3.6.X at least (I think so if I'm correct). Make sure that you have subprocess and datetime modules installed.
- low expectations

## Installation

Literally git clone this repo.

## Usage

**DO NOT USE -D and -d parameters! I did not implemented these two and thus they do not work!**

Before using it, make sure that the input mp4 file is named exactly 'orginput.mp4'. Otherwise computor will go cry and make a sad face :(
Basic usage:
```bash
python main.py -c 0 default
python main.py -c 0 lilo
```

Implemented algorithms are: default, LILO.

You can change the channels.json file to your own liking if you want as long as the whole structure is not changed :)

That's all. Fork if you want or whatever.
