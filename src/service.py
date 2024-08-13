import json
import os.path
from pathlib import Path
from typing import Any

from src.config_log import setting_log
from src.operation import find_line
from src.utils import unpack_excel

logger = setting_log("service")


def simple_find(line: str) -> Any:
    """ищет операции с заданной категорией"""
    try:
        logger.info("starting...")
        file = unpack_excel(os.path.join(Path(__file__).resolve().parents[1], "data", "operations.xls"))
        logger.info("file ready")
        json_file = json.dumps(find_line(file, line), ensure_ascii=False)
        logger.info("dumps ready")
        return json_file
    except Exception as error:
        logger.error(f"error:{error}")
        raise error
