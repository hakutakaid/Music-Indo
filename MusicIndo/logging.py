#


import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE_NAME

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

for noisy in ["httpx", "ntgcalls", "pyrogram", "pytgcalls", "pymongo"]:
    logging.getLogger(noisy).setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)