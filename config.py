

import os
import configparser


CONFIG_FILE = 'piptube.ini'
CONFIG_PATH = f"{os.environ['HOME']}/.config/piptube"
CONFIG = os.path.join(CONFIG_PATH, CONFIG_FILE)
VIDEO = 'piptube'
AUDIO = 'ytubejb'


def write_config_if_not_exists():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH, exist_ok=True)
    if not os.path.isfile(CONFIG):
        config = configparser.ConfigParser()
        config[VIDEO] = {}
        config[VIDEO]['position'] = 'bottom right'
        config[VIDEO]['video size'] = 'medium'
        config[VIDEO]['video quality'] = 'high'
        config[VIDEO]['number to play'] = '5'
        config[AUDIO] = {}
        config[AUDIO]['number to play'] = '5'
        with open(CONFIG, 'w') as configfile:
            config.write(configfile)
