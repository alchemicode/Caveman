#!/usr/bin/env python3

import yaml

from src.log import log
from src.main import bot


with open("conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)


if __name__ == "__main__":
    log()
    bot.run(config['token'])