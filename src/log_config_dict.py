from typing import Dict

log_config: Dict[str, int | bool | dict] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "default_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["default_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["default_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
