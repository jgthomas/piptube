

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
        config.set(VIDEO, '# initial location', 'top left, top right, bottom left, bottom right')
        config[VIDEO]['position'] = 'bottom right'
        config.set(VIDEO, '# initial size', 'small, medium, large, extra large')
        config[VIDEO]['video size'] = 'medium'
        config.set(VIDEO, '# quality', 'high (up to 1080p), low (480p)')
        config[VIDEO]['video quality'] = 'high'
        config[VIDEO]['number to play'] = '5'
        config[AUDIO] = {}
        config[AUDIO]['number to play'] = '5'
        with open(CONFIG, 'w') as configfile:
            config.write(configfile)
