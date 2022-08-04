import logging
import sys


def log():
    logging.basicConfig(
        level=logging.WARNING,
        format='%s(asctime)s [%(levelname)s:%(name)s] %(message)s',
        handlers=[
            logging.FileHandler("caveman.log"),
            logging.StreamHandler(sys.stderr)
        ]
    )
