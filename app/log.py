import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
import colorlog

LOGGING_FORMATTER = "%(levelname)s:     %(message)s - FILE: %(name)s - TIME: %(asctime)s"

DebugLevels = ["DEBUG", "INFO", "WARNING", "ERROR"]
DebugLevelType = str

def get_logger(
    name: Optional[str] = None,
    level: DebugLevelType = "DEBUG",
    log_file: Optional[str] = "log/app.log",
    max_bytes: int = 5_000_000,
    backup_count: int = 5
) -> logging.Logger:

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name=name)

    if logger.hasHandlers():
        return logger

    console_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(levelname)s%(reset)s:     %(message)s - FILE: %(name)s - TIME: %(asctime)s" ,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = logging.Formatter(LOGGING_FORMATTER)
    file_handler.setFormatter(file_formatter)


    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


    if not level or level not in DebugLevels:
        logger.warning(
            "Invalid logging level %s. Setting logging level to DEBUG.", level
        )
        level = "DEBUG"

    logger.setLevel(level=level)

    return logger
