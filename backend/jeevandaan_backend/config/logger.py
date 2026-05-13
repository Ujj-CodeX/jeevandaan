import json
import logging
import sys
from pythonjsonlogger import jsonlogger

def get_logger(name: str) -> logging.Logger:
    """
    Returns a JSON logger for the given module name.
    Usage: logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)
    # avouid adding multiple handlers if the logger is already configured
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        rename_fields = {
            "asctime": "timestamp",
            "levelname": "level",
            "name": "logger",
        })
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

