#!/usr/bin/env python


import subprocess
import os
import sys
import re
import argparse


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


def get_args(args):
    parser = argparse.ArgumentParser(description='Picture-in-picture video')
    parser.add_argument('source', type=str, help='file or url to play')
    return parser.parse_args(args)


def play_local(filename):
    command = [*MPV, filename]
    subprocess.run(command)


def play_url(url):
    command = [*MPV, *STREAM_URL, url]
    subprocess.run(command)


def main(argv):
    args = get_args(argv)
    to_play = args.source

    if os.path.isfile(to_play):
        play_local(to_play)
    elif re.match(r'^http', to_play):
        play_url(to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
