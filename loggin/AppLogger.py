import logging
from logging.handlers import RotatingFileHandler
from common_config import LOGGER_NAME, LOG_FILE
from os.path import exists


class AppLogger(object):

    def __init__(self):
        if not exists(LOG_FILE):
            open(LOG_FILE, 'a').close()

    @staticmethod
    def create_log():
        """
        Creates a rotating log
        """
        try:
            logger = logging.getLogger(LOGGER_NAME)
            logger.setLevel(logging.INFO)

            # add a rotating handler
            handler = RotatingFileHandler(LOG_FILE, maxBytes=200000,
                                          backupCount=5)

            handler.setFormatter(
                logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))

            logger.addHandler(handler)

            return logger

        except Exception as e:
            raise
