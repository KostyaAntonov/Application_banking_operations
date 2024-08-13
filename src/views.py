import json
import os
from pathlib import Path

import pandas as pd

from src.config_log import setting_log
from src.currency import get_currencies, get_sp500
from src.operation import find_top_transactions, info_from_operation
from src.time import find_time_of_day

loger = setting_log("views")


def major(date: str, df: pd.DataFrame) -> str:
    """
    возврощает Json-ответ с информацией на главной
    :param date: дата
    :param df: датафрейм с операциями
    :return: возврощает json-ответ
    """
    with open(os.path.join(Path(__file__).resolve().parents[1], "user_settings.json")) as f:
        loger.info("loading_json...")
        info = json.load(f)
    loger.info("get greeting...")
    greeting = find_time_of_day(date)
    list_currency = info["user_currencies"]
    list_stocks = info["user_stocks"]
    loger.info("get data...")
    data = df.to_dict(orient="records")
    loger.info("load operation..")
    list_operation = info_from_operation(data, date)
    loger.info("load top...")
    top = find_top_transactions(data, date)
    loger.info("load currecies...")
    currency = get_currencies(list_currency)
    loger.info("get sp500...")
    sp500 = get_sp500(list_stocks)
    json_file = {
        "greeting": greeting,
        "cards": list_operation,
        "top_transactions": top,
        "currency_rates": currency,
        "stock_prices": sp500,
    }
    return json.dumps(json_file, ensure_ascii=False)
