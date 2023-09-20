import logging

from utils.envs import LOG_LEVEL


def rayserve_logger():
    logger = logging.getLogger("ray.serve")
    log_level = logging_level()

    logger.setLevel(log_level)
    return logger


def logging_level():
    return logging.INFO if LOG_LEVEL is None else LOG_LEVEL
