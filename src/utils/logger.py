import logging
import sys


def create_logger():

    logger = logging.getLogger(
        "CyberSentinelAI"
    )

    if logger.handlers:
        return logger


    logger.setLevel(
        logging.INFO
    )


    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )


    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(
        formatter
    )


    logger.addHandler(
        handler
    )


    return logger



logger = create_logger()