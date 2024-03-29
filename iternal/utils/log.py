import logging
import sys

from loguru import logger

from iternal import config


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


# noinspection PyArgumentList
def setup(disable: list = None, log_format: str = None):
    logger.add(sys.stderr, format=log_format or "{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(config.LOGS_BASE_PATH + "/file_{time}.log")
    logger.disable("sqlalchemy")
    if disable is not None:
        for d in disable:
            logger.disable(d)
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
