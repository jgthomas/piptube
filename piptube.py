#!/usr/bin/env python


import subprocess
import os
import sys
import re
import argparse
import configparser


APP_NAME = 'piptube'

CONFIG = 'piptube.ini'

BASE = {'size': 'medium',
        'quality': 'high',
        'position': 'bottom right',
        'number': 5}

VIDEO_SIZE = {'small': '384x216',
              'medium': '640x360',
              'large': '1280x720',
              'extra large': '1920x1080'}

VIDEO_POSITION = {'top left': '2%:2%',
                  'top right': '98%:2%',
                  'bottom right': '98%:98%',
                  'bottom left': '2%:98%'}

VIDEO_QUALITY = {'low': '(mp4)[height<=480]/best[height<=480]',
                 'high': '(mp4)[height<=1080]/best[height<=1080]'}


def get_args(args):
    parser = argparse.ArgumentParser(description='Picture-in-picture video')
    parser.add_argument('source', type=str, help='file or url to play')
    parser.add_argument('-n', '--number-to-play', type=int, help='number of videos to play', metavar='')
    parser.add_argument('-lq', '--low-quality', action='store_true', help='use a lower quality steam')
    size = parser.add_mutually_exclusive_group()
    size.add_argument('-s', '--small', action='store_true', help='small video')
    size.add_argument('-m', '--medium', action='store_true', help='medium video')
    size.add_argument('-l', '--large', action='store_true', help='large video')
    size.add_argument('-xl', '--extra-large', action='store_true', help='extra large video')
    position = parser.add_mutually_exclusive_group()
    position.add_argument('-tl', '--top-left', action='store_true', help='initial placement top left')
    position.add_argument('-tr', '--top-right', action='store_true', help='initial placement top right')
    position.add_argument('-bl', '--bottom-left', action='store_true', help='initial placement bottom left')
    position.add_argument('-br', '--bottom-right', action='store_true', help='initial placement bottom right')
    return parser.parse_args(args)


class PlayVideo:

    MPV_BASE = ['mpv',
                '--ontop',
                '--no-border',
                '--on-all-workspaces'
                ]

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
        self.mpv = [*self.MPV_BASE, self.size, self.position]
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
    config = configparser.ConfigParser()
    config.read(CONFIG)
    config_specified = True

    args = get_args(argv)

    source = args.source

    # source type
    if os.path.isfile(source):
        source_type = 'file'
    elif re.match(r'^http', source):
        source_type = 'url'
    else:
        source_type = 'search'

    # video size
    if args.small:
        size = VIDEO_SIZE['small']
    elif args.medium:
        size = VIDEO_SIZE['medium']
    elif args.large:
        size = VIDEO_SIZE['large']
    elif args.extra_large:
        size = VIDEO_SIZE['extra large']
    else:
        try:
            default_size = config[APP_NAME]['video size']
            size = VIDEO_SIZE[default_size]
        except KeyError:
            print('Size not specifed, reverting to built-in default...')
            config_specified = False
            size = VIDEO_SIZE[BASE['size']]

    # video position
    if args.top_left:
        position = VIDEO_POSITION['top left']
    elif args.top_right:
        position = VIDEO_POSITION['top right']
    elif args.bottom_left:
        position = VIDEO_POSITION['bottom left']
    elif args.bottom_right:
        position = VIDEO_POSITION['bottom right']
    else:
        try:
            default_position = config[APP_NAME]['position']
            position = VIDEO_POSITION[default_position]
        except KeyError:
            print('Position not specifed, reverting to built-in default...')
            config_specified = False
            position = VIDEO_POSITION[BASE['position']]

    # number of videos to play
    if args.number_to_play:
        number_to_play = args.number_to_play
    else:
        try:
            number_to_play = config[APP_NAME]['number to play']
        except KeyError:
            print('Number to play not specifed, reverting to built-in default...')
            config_specified = False
            number_to_play = BASE['number']

    # video quality
    if args.low_quality:
        video_format = VIDEO_QUALITY['low']
    else:
        try:
            default_quality = config[APP_NAME]['video quality']
            video_format = VIDEO_QUALITY[default_quality]
        except KeyError:
            print('Quality not specifed, reverting to built-in default...')
            config_specified = False
            video_format = VIDEO_QUALITY[BASE['quality']]

    if not config_specified:
        print(f'Pass settings via command line, or place settings in "{CONFIG}"')

    PlayVideo(source,
              source_type,
              size,
              position,
              video_format,
              number_to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
