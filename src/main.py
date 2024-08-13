import json
import os.path

import pandas as pd

from src.reports import spending_by_category
from src.service import simple_find
from src.views import major


def main() -> None:
    print("Главная")
    print("Введите дату в формате YYYY-MM-DD HH:MM:SS")
    date = input()
    df = pd.read_excel(os.path.join("../data", "operations.xls"), na_filter=False)
    print(json.loads(major(date, df)))
    print()
    print("Простой поиск")
    print("Введите строку которую надо найти в описании или категории")
    line = input()
    print(json.loads(simple_find(line)))
    print()
    print("Отчеты")
    print("Введите категорию по которой вы ходите увидеть отчеты")
    df = pd.read_excel(os.path.join("../data", "operations.xls"))
    category = input()
    print(json.loads(spending_by_category(df, category, date)))


if __name__ == "__main__":
    main()
