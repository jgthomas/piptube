#!/usr/bin/env python


import subprocess
import os
import sys
import re
import argparse


LOW_FORMAT = '(mp4)[height<=480]/best[height<=480]'
NORMAL_FORMAT = '(mp4)[height<=1080]/best[height<=1080]'
FORMAT = NORMAL_FORMAT

SMALL_VID = '384x216'
MED_VID = '640x360'
LARGE_VID ='1280x720'
SIZE = MED_VID

TOP_RIGHT = '98%:2%'
BOTTOM_RIGHT = '98%:98%'
TOP_LEFT = '2%:2%'
BOTTOM_LEFT = '2%:98%'
POSITION = BOTTOM_RIGHT

VIDEO_NO = 5

MPV = ['mpv',
       '--ontop',
       '--no-border',
       '--on-all-workspaces',
       f'--autofit={SIZE}',
       f'--geometry={POSITION}'
       ]


STREAM_URL = ['--ytdl-format', f'{FORMAT}']

STREAM_SEARCH = ['youtube-dl',
                 '--format',
                 f'{FORMAT}',
                 '--get-url'
                 ]


def get_args(args):
    parser = argparse.ArgumentParser(description='Picture-in-picture video')
    parser.add_argument('source', type=str, help='file or url to play')
    return parser.parse_args(args)


def play_local(filename):
    command = [*MPV, filename]
    subprocess.run(command)


def stream_url(url):
    command = [*MPV, *STREAM_URL, url]
    subprocess.run(command)


def stream_search(s):
    search = f'ytsearch{VIDEO_NO}:{s}'
    search_command = [*STREAM_SEARCH, search]
    search_results = subprocess.Popen(search_command, stdout=subprocess.PIPE)
    output, _ = search_results.communicate()
    to_play = output.split(b'\n')
    subprocess.run([*MPV, *to_play])


def main(argv):
    args = get_args(argv)
    to_play = args.source

    if os.path.isfile(to_play):
        play_local(to_play)
    elif re.match(r'^http', to_play):
        stream_url(to_play)
    else:
        stream_search(to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
