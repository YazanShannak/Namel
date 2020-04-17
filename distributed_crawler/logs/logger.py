import logging


class Logger:
    def __init__(self, name):
        self.name = name
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log(self, message):
        self.logger.debug(message)
