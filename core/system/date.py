from datetime import datetime
from loguru import logger


MONTHS_GENITIVE = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def plural(n: int, forms: tuple[str, str, str]) -> str:
    if 11 <= n % 100 <= 14:
        return forms[2]
    if n % 10 == 1:
        return forms[0]
    if 2 <= n % 10 <= 4:
        return forms[1]
    return forms[2]


def today() -> str:
    time = datetime.now()

    day = time.day
    month = MONTHS_GENITIVE[time.month]

    return f"{day} {month}"


def normal_time(time) -> str:
    minutes = (time % 3600) // 60
    hours = time // 3600

    t_h = plural(hours, ("час", "часа", "часов"))
    t_m = plural(minutes, ("минута", "минуты", "минут"))

    res = f"{hours} {t_h} {minutes} {t_m}"

    return res


def to_time(time: int, format: str = 'h') -> int:
    if format == 'h':
        return time // 3600
    elif format == 'm':
        return (time % 3600) // 60
    else:
        logger.debug("Неверный аргумент времени")