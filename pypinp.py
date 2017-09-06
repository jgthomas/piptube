#!/usr/bin/env python


import subprocess
import os
import sys
import re


MPV = ['mpv',
       '--ontop',
       '--no-border',
       '--on-all-workspaces',
       '--autofit=640x320',
       '--geometry=98%:98%'
       ]


STREAM_URL = ['--ytdl-format',
              '(mp4)[height<=1080]/best[height<=1080]'
              ]


def play_local(filename):
    MPV.append(filename)
    subprocess.run(MPV)


def play_url(url):
    command = MPV + STREAM_URL
    command.append(url)
    subprocess.run(command)


def main(argv):
    to_play = argv[0]

    if os.path.isfile(to_play):
        play_local(to_play)
    elif re.match(r'^http', to_play):
        play_url(to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
