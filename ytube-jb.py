#!/usr/bin/env python


import subprocess
import os
import sys
import re
import argparse
import configparser

APP = 'ytube-jb'

CONFIG = 'piptube.ini'

BASE = {'number': 5}


def get_args(args):
    parser = argparse.ArgumentParser(description='YouTube as a command line jukebox')
    parser.add_argument('source', type=str, help='file or url to play')
    parser.add_argument('-n', '--number-to-play', type=int, help='number of streams to play', metavar='')
    return parser.parse_args(args)
 

class PlayAudio:

    def __init__(self, source, source_type, number_to_play):
        self.source = source
        self.source_type = source_type
        self.number_to_play = number_to_play
        self.play_audio()

    def play_url(self):
        subprocess.run(['mpv', '--no-video', self.source])

    def play_search_result(self):
        search = f'ytsearch{self.number_to_play}:{self.source}'
        search_command = ['youtube-dl',
                          '--format',
                          'bestaudio',
                          '--get-url',
                          search]
        search_results = subprocess.Popen(search_command,
                                          stdout=subprocess.PIPE)
        output, _ = search_results.communicate()
        to_play = output.split(b'\n')
        subprocess.run(['mpv', *to_play])

    def play_audio(self):
        play = {'url': self.play_url,
                'search': self.play_search_result}
        play[self.source_type]()


def main(argv):
    config = configparser.ConfigParser()
    config.read(CONFIG)
    config_specified = True

    args = get_args(argv)

    source = args.source

    if re.match(r'^http', source):
        source_type = 'url'
    else:
        source_type = 'search'

    if args.number_to_play:
        number_to_play = args.number_to_play
    else:
        try:
            number_to_play = config[APP]['number to play']
        except KeyError:
            print('Number to play not specified, reverting to built-in default...')
            config_specified = False
            number_to_play = BASE['number']

    if not config_specified:
        print(f'Pass settings via command line, or edit settings in "{CONFIG}"')

    PlayAudio(source, source_type, number_to_play)


if __name__ == '__main__':
    main(sys.argv[1:])
