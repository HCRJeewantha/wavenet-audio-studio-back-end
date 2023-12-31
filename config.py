# config.py
from pydantic import BaseModel


class LogConfig(BaseModel):

    LOGGER_NAME: str = "audio-studio"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }

    loggers = {
        "audio-studio": {"handlers": ["default"], "level": LOG_LEVEL},
    }


# global instance
logConfig = LogConfig()
