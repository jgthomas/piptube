

import os
import configparser


CONFIG = 'piptube.ini'
VIDEO = 'piptube'
AUDIO = 'ytubejb'


def write_config_if_not_exists(inifile):
    if not os.path.isfile(inifile):
        config = configparser.ConfigParser()
        config[VIDEO] = {}
        config[VIDEO]['position'] = 'bottom right'
        config[VIDEO]['video size'] = 'medium'
        config[VIDEO]['video quality'] = 'high'
        config[VIDEO]['number to play'] = '5'
        config[AUDIO] = {}
        config[AUDIO]['number to play'] = '5'
        with open(inifile, 'w') as configfile:
            config.write(configfile)
