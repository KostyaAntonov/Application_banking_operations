import os.path
import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from src.config_log import setting_log
from src.utils import write_xml_from_web

logger = setting_log("currency")

# словарь код валюты: ID валюты
CODE_CURRENCY = {
    "AUD": "R01010",
    "AZN": "R01020A",
    "GBP": "R01035",
    "AMD": "R01060",
    "BYN": "R01090B",
    "BGN": "R01100",
    "BRL": "R01115",
    "HUF": "R01135",
    "VND": "R01150",
    "HKD": "R01200",
    "GEL": "R01210",
    "DKK": "R01215",
    "AED": "R01230",
    "USD": "R01235",
    "EUR": "R01239",
    "EGP": "R01240",
    "INR": "R01270",
    "IDR": "R01280",
    "KZT": "R01335",
    "CAD": "R01350",
    "QAR": "R01355",
    "KGS": "R01370",
    "CNY": "R01375",
    "MDL": "R01500",
    "NZD": "R01530",
    "NOK": "R01535",
    "PLN": "R01565",
    "RON": "R01585F",
    "XDR": "R01589",
    "SGD": "R01625",
    "TJS": "R01670",
    "THB": "R01675",
    "TRY": "R01700J",
    "TMT": "R01710A",
    "UZS": "R01717",
    "UAH": "R01720",
    "CZK": "R01760",
    "SEK": "R01770",
    "CHF": "R01775",
    "RSD": "R01805F",
    "ZAR": "R01810",
    "KRW": "R01815",
    "JPY": "R01820",
}


def get_currencies(currency: list) -> list | bool | Any:
    """
    находит в xml файле цену этой валюты в рублях
    :param currency: валюта
    :return: цена валюты
    """
    list_currency = []
    if "RUB" in currency:
        logger.info("currency is RUB")
        list_currency.append({"currency": "RUB", "rate": "1"})
    currency = list(map(lambda x: CODE_CURRENCY.get(x, ""), currency))
    # получает актуальную дату
    time_now = datetime.strftime(datetime.now(), "%d/%m/%Y")
    # использую дату как ссылку для xml данных центра банка
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={time_now}"
    # функция которая записывает xml с айта
    write_xml_from_web(url, "cbr")
    # парсим данные с нашего файла
    logger.info("parse data...")
    three = ET.parse(os.path.join(Path(__file__).resolve().parents[1], "data", "cbr.xml"))
    # получаем корневой элемент
    root = three.getroot()
    # проходимся по корню`
    for child in root:
        if child.attrib["ID"] in currency:
            for item in child:
                if item.tag == "Value":
                    element = item.text
                elif item.tag == "CharCode":
                    code = item.text
            if element is not None and code is not None:
                value_currency = str(Decimal(str(element).replace(",", ".")))
                logger.info(f"good parse value is {str(value_currency)}")
                list_currency.append({"currency": code, "rate": value_currency})
    return list_currency


def get_sp500(stocks: list) -> list[dict]:
    """
    берет курс акций из S&P500
    :param stocks: лист акций которые нужны
    :return: список с словарями с названием и ценой
    """
    list_stock = []
    load_dotenv()
    API = os.getenv("API")
    logger.info("get API...")
    for element in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={element}&apikey={API}"
        logger.info("request...")
        info = requests.get(url).json()
        last_ref = info["Meta Data"]["3. Last Refreshed"]
        close = info["Time Series (Daily)"][last_ref]["4. close"]
        logger.info("done")
        list_stock.append({"stock": element, "price": close})
    return list_stock
