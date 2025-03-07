# An application for analyzing banking transactions

Pycharm Project

## Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

### *Страница «Главная»*. набор функций и главную функция, принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:

1. Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.

2. По каждой карте:
 - последние 4 цифры карты;
 - общая сумма расходов;
 - кешбэк (1 рубль на каждые 100 рублей).
 - Топ-5 транзакций по сумме платежа.
3. Курс валют.

4. Стоимость акций из S&P500.

### *«Сервисы»*. Простой поиск. Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории.

### *«Отчёты»*. Траты по дням недели. 
Функция принимает на вход:

 - датафрейм с транзакциями,
 - опциональную дату.
 - Если дата не передана, то берется текущая дата.

Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
