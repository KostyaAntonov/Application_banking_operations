import datetime
import typing
from functools import wraps


def log(*, filename: str = "log_you_func") -> typing.Callable:
    """
    декоратор, который пишет информацию о работе функции если, указать имя файла
    то напишет текстовый файл в той же дериктории, где вызвана функция,
    если же не указать напишет в файл под заданным назаванием.


    filename: str | None аргумент, который принимает имя файла, если его не написать то принимает NONE
    и выводит информацию о работе функции в консоль
    """

    def wrapper(func: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Any], str]:
        @wraps(func)
        def init(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            with open(f"{filename}.log", "a", encoding="utf8") as file:
                try:
                    res = func(*args, **kwargs)
                except Exception as exeption:
                    # time - берет актуальное время и форматирует его по формуле
                    # type(exeption).__name__ - получает имя ошибки
                    time = str(datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S"))
                    file.write(
                        f"{time} {func.__name__} error: {type(exeption).__name__}\n"
                        f"full error: {exeption}\n"
                        f"{'!' * 50}"
                        f"{type(exeption).__name__}"
                        f"{'!' * 50}\n"
                    )

                else:
                    time = str(datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S"))
                    file.write(f"{time} {func.__name__} ok\nresult: {res}\n{'=' * 50} passed {'=' * 50}\n")
                    return res

        return init

    return wrapper
