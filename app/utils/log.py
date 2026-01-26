import logging

logger = logging.getLogger(__name__)

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def log_handler(level: str, message: str, exception: Exception | None = None):
    log_level = LOG_LEVELS.get(level.lower(), logging.INFO)

    if exception:
        logger.log(log_level, message, exc_info=exception)
    else:
        logger.log(log_level, message)
