import json
from datetime import datetime
from typing import Optional

import pandas as pd

from src.config_log import setting_log
from src.operation import find_category_df
from src.time import find_range_time_df, range_time

logger = setting_log("reports")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """
    возвращает траты по заданной категории за последние три месяца от переданной даты
    :param transactions: датафрейм операций
    :param category: категория
    :param date: дата если дата не подается то берется текушая
    :return: возврощает датафрейм
    """
    try:
        transactions = transactions[transactions["Сумма платежа"] < 0]
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"get now time: {date}")
        list_time = range_time(date, 3)
        logger.info("find category...")
        transactions = find_category_df(transactions, category)
        logger.info("find time range...")
        transactions = find_range_time_df(transactions, list_time)
        logger.info("done")
        return json.dumps(transactions.to_json(force_ascii=False, orient="records"), ensure_ascii=False)
    except Exception as error:
        logger.error(f"error:{error}")
        raise error
