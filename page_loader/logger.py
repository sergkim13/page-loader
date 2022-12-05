import logging
import logging.config


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(levelname)s - %(name)s:%(lineno)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
