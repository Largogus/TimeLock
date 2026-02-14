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


def normal_time(time: int, format: str = "standard") -> str:
    """:param format: standard - '7 часов' , full - '7 часов 0 минут', short - '7ч'"""

    minutes = (time % 3600) // 60
    hours = time // 3600

    f_h = plural(hours, ("час", "часа", "часов")) if format in ("standard", "full") else "ч"
    f_m = plural(minutes, ("минута", "минуты", "минут")) if format in ("standard", "full") else "м"

    if minutes == 0 and format != 'full':
        return f"{hours} {f_h}"

    if hours == 0 and format != 'full':
        return f"{minutes} {f_m}"

    res = f"{hours} {f_h} {minutes} {f_m}"

    return res


def to_time(time: int, format: str = 'h') -> int:
    if format == 'h':
        return time // 3600
    elif format == 'm':
        return (time % 3600) // 60
    else:
        logger.debug("Неверный аргумент времени")


def parse_time(text: str) -> int:
    '''4м -> 2400с'''

    if text == "0" or text == "Нет":
        return 0
    hours, minutes = 0, 0
    if "ч" in text:
        hours_part = text.split("ч")[0]
        hours = int(hours_part)
        text = text.split("ч")[1]
    if "м" in text:
        minutes_part = text.split("м")[0]
        minutes = int(minutes_part)
    return hours * 60 + minutes