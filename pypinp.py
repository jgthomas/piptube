#!/usr/bin/env python


import subprocess
import os
import sys
import re
import argparse


LOW_FORMAT = '(mp4)[height<=480]/best[height<=480]'
NORMAL_FORMAT = '(mp4)[height<=1080]/best[height<=1080]'
DEFAULT_FORMAT = NORMAL_FORMAT

SMALL_VIDEO = '384x216'
MEDIUM_VIDEO = '640x360'
LARGE_VIDEO ='1280x720'
DEFAULT_VIDEO = MEDIUM_VIDEO

TOP_RIGHT = '98%:2%'
BOTTOM_RIGHT = '98%:98%'
TOP_LEFT = '2%:2%'
BOTTOM_LEFT = '2%:98%'
DEFAULT_POSITION = BOTTOM_RIGHT

DEFAULT_NUMBER = 5

MPV_BASE = ['mpv',
            '--ontop',
            '--no-border',
            '--on-all-workspaces'
            ]


def get_args(args):
    parser = argparse.ArgumentParser(description='Picture-in-picture video')
    parser.add_argument('source', type=str, help='file or url to play')
    parser.add_argument('-n', '--number-to-play', type=int, help='number of videos to play', metavar='')
    parser.add_argument('-lq', '--low-quality', action='store_true', help='use a lower quality steam')
    size = parser.add_mutually_exclusive_group()
    size.add_argument('-s', '--small', action='store_true', help='small video')
    size.add_argument('-m', '--medium', action='store_true', help='medium video')
    size.add_argument('-l', '--large', action='store_true', help='large video')
    position = parser.add_mutually_exclusive_group()
    position.add_argument('-tl', '--top-left', action='store_true', help='initial placement top left')
    position.add_argument('-tr', '--top-right', action='store_true', help='initial placement top right')
    position.add_argument('-bl', '--bottom-left', action='store_true', help='initial placement bottom left')
    position.add_argument('-br', '--bottom-right', action='store_true', help='initial placement bottom right')
    return parser.parse_args(args)


class PlayVideo:

    def __init__(self,
                 source,
                 source_type,
                 size,
                 position,
                 video_format,
                 number_to_play):
        self.source = source
        self.source_type = source_type
        self.size = f'--autofit={size}'
        self.position = f'--geometry={position}'
        self.video_format = f'{video_format}'
        self.number_to_play = number_to_play
        self.mpv = [*MPV_BASE, self.size, self.position]
        self.play_video()

    def play_local(self):
        subprocess.run([*self.mpv,
                        self.source])

    def play_url(self):
        subprocess.run([*self.mpv,
                        '--ytdl-format',
                        self.video_format,
                        self.source])

    def play_search_result(self):
        search = f'ytsearch{self.number_to_play}:{self.source}'
        search_command = ['youtube-dl',
                          '--format',
                          self.video_format,
                          '--get-url',
                          search]
        search_results = subprocess.Popen(search_command,
                                          stdout=subprocess.PIPE)
        output, _ = search_results.communicate()
        to_play = output.split(b'\n')
        subprocess.run([*self.mpv, *to_play])

    def play_video(self):
        play = {'file': self.play_local,
                'url': self.play_url,
                'search': self.play_search_result}
        play[self.source_type]()


def main(argv):
    args = get_args(argv)

    source = args.source

    # detect type of source
    if os.path.isfile(source):
        source_type = 'file'
    elif re.match(r'^http', source):
        source_type = 'url'
    else:
        source_type = 'search'

    # video size
    if args.small:
        size = SMALL_VIDEO
    elif args.medium:
        size = MEDIUM_VIDEO
    elif args.large:
        size = LARGE_VIDEO
    else:
        size = DEFAULT_VIDEO

    # video position
    if args.top_left:
        position = TOP_LEFT
    elif args.top_right:
        position = TOP_RIGHT
    elif args.bottom_left:
        position = BOTTOM_LEFT
    elif args.bottom_right:
        position = BOTTOM_RIGHT
    else:
        position = DEFAULT_POSITION

    # number of videos to play
    if args.number_to_play:
        number_to_play = args.number_to_play
    else:
        number_to_play = DEFAULT_NUMBER

    # video quality and format
    if args.low_quality:
        video_format = LOW_FORMAT
    else:
        video_format = DEFAULT_FORMAT

    PlayVideo(source,
              source_type,
              size,
              position,
              video_format,
              number_to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
