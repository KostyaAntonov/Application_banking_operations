from datetime import datetime, timedelta

import pandas as pd

from src.config_log import setting_log

loger = setting_log("time")


def find_time_of_day(date: str) -> str:
    """
    пишет Доброе утро/Добрый день/Добрый вечер/Доброй ночи в зависимости от времени
    :param date: дата и время в формате YYYY-MM-DD HH:MM:SS
    :return: Доброе утро/Добрый день/Добрый вечер/Доброй ночи
    """
    try:
        loger.info("checking time...")
        date_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%H")
        if 4 <= int(date_object) <= 11:
            loger.info("return Доброе утро")
            return "Доброе утро"
        elif 12 <= int(date_object) <= 16:
            loger.info("return Добрый день")
            return "Добрый день"
        elif 17 <= int(date_object) <= 23:
            loger.info("return Добрый вечер")
            return "Добрый вечер"
        elif 0 <= int(date_object) <= 3:
            loger.info("return Доброй ночи")
            return "Доброй ночи"
        loger.info("unknown return Добро пожаловать")
        return "Добро пожаловать"
    except Exception as error:
        loger.error(f"error: {error}")
        raise error


def range_time(date: str, mouth: int = 1) -> list:
    """
    находит диапазон дат в радиусе месяца
    :param mouth: диапазон
    :param date: дата и время в формате YYYY-MM-DD HH:MM:SS
    :return: список с датами в формате M D Y
    """
    try:
        loger.info("checking time...")
        base = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_list = []
        for _ in range(mouth):
            b1 = int(base.strftime("%m"))
            b = int(base.strftime("%m"))
            loger.info("search range...")
            while b == b1:
                date_list.append(base.strftime("%m %d %Y"))
                base = base - timedelta(days=1)
                b = int(base.strftime("%m"))
        loger.info(f"range {date_list}")
        return date_list
    except Exception as error:
        loger.error(f"error:{error}")
        raise error


def find_range_time(operation: list[dict], date_list: list) -> list[dict]:
    """
    находит даты которое есть в диапозоне
    :param operation: лист с словарями в котором хранятся операции
    :param date_list: лист с датами в формате M D Y
    :return: лист с словарями которые находятся в диапозоне
    """
    try:
        new_list = []
        loger.info("find operation...")
        for item in operation:
            if item["Дата платежа"]:
                date = datetime.strptime(item["Дата платежа"], "%d.%m.%Y").strftime("%m %d %Y")
                if date in date_list:
                    new_list.append(item)
        loger.info(f"find {len(new_list)} operation!")
        return new_list
    except Exception as error:
        loger.error(f"error:{error}")
        raise error


def find_range_time_df(df: pd.DataFrame, date_list: list) -> pd.DataFrame:
    """
    отстовляет строки которые в диапозоне заданного времени
    :param df: дата фрейм с операциями
    :param date_list:дипозон дат
    :return: датофрейм в диапозоне дат
    """
    try:
        df = df[pd.to_datetime(df["Дата операции"], dayfirst=False).dt.strftime("%m %d %Y").isin(date_list)]
        return df
    except Exception as error:
        loger.error(f"error:{error}")
        raise error
