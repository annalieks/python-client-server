import logging


class Logger:
    def __init__(self, logfile, level=None):
        self._logger = logging.getLogger()
        handler = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(level or logging.INFO)

    def get(self):
        return self._logger
