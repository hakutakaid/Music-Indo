#
#
import logging
import sys

from pymongo import AsyncMongoClient

import config

DB_NAME = "Yukki"

if config.MONGO_DB_URI is None:
    logging.getLogger(__name__).error(
        "No MongoDB URL found. Please add your MongoDB URL before running the bot. Exiting."
    )
    sys.exit(1)

mongo_client = AsyncMongoClient(config.MONGO_DB_URI)
mongodb = mongo_client[DB_NAME]
