

import os
import configparser


def write_config_if_not_exists(inifile):
    if not os.path.isfile(inifile):
        config = configparser.ConfigParser()
        config['piptube'] = {}
        config['piptube']['position'] = 'bottom right'
        config['piptube']['video size'] = 'medium'
        config['piptube']['video quality'] = 'high'
        config['piptube']['number to play'] = '5'
        config['ytube-jb'] = {}
        config['ytube-jb']['number to play'] = '5'
        with open(inifile, 'w') as configfile:
            config.write(configfile)
