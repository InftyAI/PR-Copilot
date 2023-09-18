import logging

from utils.envs import LOG_LEVEL


def logging_level():
    return logging.INFO if LOG_LEVEL is None else LOG_LEVEL


logger = logging.getLogger("pr-copilot")
logger.setLevel(logging_level())
