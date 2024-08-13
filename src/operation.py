from decimal import Decimal

import pandas as pd

from src.config_log import setting_log
from src.time import find_range_time, range_time

logger = setting_log("operation")


def info_from_operation(operation: list[dict], date: str) -> list[dict]:
    """
    находит общую сумму всех операция по каждой карте
    :param operation: данные операций
    :param date дата от которой идет отсчет
    :return: список с словорями с информацией о операциях по каждой карте
    """
    try:
        logger.info("find operation...")
        operation = find_range_time(operation, range_time(date))
        sum_cashback = 0
        info_card: dict = {}
        for item in operation:
            # берем только траты
            if int(item["Сумма операции"]) < 0:
                if operation:
                    name = item["Номер карты"]
                    # проверяем указана ли карта
                    if len(name) >= 4:
                        name = name[-4:]
                        sum_operation = (info_card.get(name, {}).get("total_spent", 0)) + (
                            Decimal(str(item["Сумма операции"])) * -1
                        )
                        if sum_operation >= 100:
                            logger.info(f'sum operation: {str(item["Сумма операции"] * -1)} > 100 add cashback')
                            sum_cashback = info_card.get(name, {}).get("cashback", 0) + (
                                Decimal(str(item["Сумма операции"])) * -1 / 100
                            )
                        info_card[name] = {"total_spent": sum_operation, "cashback": sum_cashback}

                    else:
                        logger.info("card don't have name maybe it's transfer")
                        name = "Переводы"
                        sum_operation = (info_card.get(name, {}).get("total_spent", 0)) + (
                            Decimal(str(item["Сумма операции"])) * -1
                        )
                        info_card["Переводы"] = {"total_spent": sum_operation, "cashback": 0}
        # формируем список
        logger.info("formatting list")
        list_info = []
        for k, v in info_card.items():
            list_info.append(
                {
                    "last_digits": k,
                    "total_spent": str(info_card[k]["total_spent"]),
                    "cashback": str(info_card[k]["cashback"]),
                }
            )
        logger.info(f"create data count cart{len(list_info)}")
        return list_info
    except Exception as error:
        logger.error(f"operation error: {error}")
        raise error


def find_top_transactions(operation: list[dict], date: str, top: int = 5) -> list[dict]:
    """
    находит топ транзакий в диапозоне даты
    :param operation данные операций
    :param date дата
    :param top число топов
    :return список с топом операций
    """
    try:
        top_list = []
        # берем только траты
        logger.info("getting operation...")
        operation = list(filter(lambda x: int(x["Сумма операции"]) < 0, operation))
        operation = find_range_time(operation, range_time(date))
        # проверка на топ
        if top > len(operation):
            logger.info("user top > length operations")
            top = len(operation)
        # находим топ
        for _ in range(top):
            if operation:
                leader = operation.pop(operation.index(max(operation, key=lambda x: x["Сумма операции"] * -1)))
                top_list.append(
                    {
                        "date": leader["Дата платежа"],
                        "amount": float(leader["Сумма операции"]) * -1,
                        "category": leader["Категория"],
                        "description": leader["Описание"],
                    }
                )
                logger.info("new top find!")
        logger.info(f"top length: {len(top_list)}")
        return top_list
    except Exception as error:
        logger.error(f"error: {error}")
        raise error


def find_line(operation: list[dict], line: str) -> list[dict]:
    """находит словари с тем что поддал пользователь"""
    try:
        logger.info("getting operations...")
        new_data = []
        for item in operation:
            if line.lower() in item["Категория"].lower() or line.lower() in item["Описание"].lower():
                new_data.append(item)
        logger.info("find line!")
        return new_data
    except Exception as error:
        logger.error(f"error: {error}")
        raise error


def find_category_df(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    ищет стороки с категориями
    :param df: датафрейм
    :param category: категория по которой идет поиск
    :return: отфильтрованный датафрейм
    """
    try:
        df = df[df["Категория"].str.lower() == category.lower()]
        logger.info("find done")
        return pd.DataFrame(df)
    except Exception as error:
        logger.error(f"error: {error}")
        raise error
