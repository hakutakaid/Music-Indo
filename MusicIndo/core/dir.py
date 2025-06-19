#
#
import logging
import os
from os import listdir, mkdir

# remove all files on startup  that contains these extentions
files = [
    ".jpg",
    ".jpeg",
    ".mp3",
    ".m4a",
    ".mp4",
    ".webm",
    ".png",
]


def dirr():
    downloads_folder = "downloads"
    cache_folder = "cache"

    for file in os.listdir():
        if any(file.endswith(ext) for ext in files):
            os.remove(file)

    if downloads_folder not in listdir():
        mkdir(downloads_folder)

    if cache_folder not in listdir():
        mkdir(cache_folder)

    logging.info("Directories Updated.")
