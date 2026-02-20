# logging_config.py
import logging
from logging.handlers import TimedRotatingFileHandler

def get_daily_logger(nombre_log="app", archivo="app.log"):
    logger = logging.getLogger(nombre_log)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            archivo,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger