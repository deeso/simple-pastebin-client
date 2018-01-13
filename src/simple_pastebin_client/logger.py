import logging
import sys
from simple_pastebin_scraper import consts


def init_logger(name=consts.NAME,
                log_level=logging.DEBUG,
                logging_fmt=consts.LOGGING_FORMAT):

    if name != consts.NAME and consts.LOGGER is None:
        init_logger(log_level=log_level, logging_fmt=logging_fmt)

    logging.getLogger(name).setLevel(log_level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    formatter = logging.Formatter(logging_fmt)
    ch.setFormatter(formatter)
    logging.getLogger(name).addHandler(ch)

    if name == consts.NAME:
        consts.LOGGER = logging.getLogger(name)


def logger(name=consts.NAME):
    if consts.LOGGER is None:
        init_logger()
    if name != consts.NAME:
        return logging.getLogger(name)
    return consts.LOGGER


def debug(msg):
    logger().debug(msg)


def info(msg):
    logger().info(msg)


def warn(msg):
    logger().warn(msg)
