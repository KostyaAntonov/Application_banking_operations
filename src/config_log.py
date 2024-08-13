import logging
import os.path
from pathlib import Path
from typing import Any


def setting_log(name: Any) -> logging.Logger:
    """настройки логера"""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(
        f"{os.path.join(Path(__file__).resolve().parents[1], 'log', name)}.log", "w", encoding="utf-8"
    )
    file_formatter = logging.Formatter("%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
