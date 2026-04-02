from datetime import datetime
from PySide6.QtCore import QTime
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


def normal_time(time: int, format: str = "standard", with_sec: bool = False) -> str:
    """:param format: standard - '7 часов' , full - '7 часов 0 минут', short - '7ч'"""

    minutes = int((time % 3600) // 60)
    hours = int(time // 3600)
    seconds = time % 60

    f_h = plural(hours, ("час", "часа", "часов")) if format in ("standard", "full") else "ч"
    f_m = plural(minutes, ("минута", "минуты", "минут")) if format in ("standard", "full") else "м"
    f_s = plural(seconds, ("секунда", "секунды", "секунд")) if format in ("standard", "full") else "с"

    if format == "short":
        parts = []
        if hours > 0:
            parts.append(f"{hours} ч")
        if minutes > 0:
            parts.append(f"{minutes} м")
        if with_sec and seconds > 0:
            parts.append(f"{seconds} с")
        return " ".join(parts) if parts else "0 м"

    if format == "standard":
        if hours > 0 and minutes == 0:
            return f"{hours} {f_h}"
        if hours == 0 and minutes >= 0 and not with_sec:
            return f"{minutes} {f_m}"
        if hours == 0 and minutes > 0 and with_sec:
            return f"{minutes} {f_m}"
        if hours == 0 and minutes == 0 and with_sec:
            return f"{seconds} {f_s}"
        return f"{hours} {f_h} {minutes} {f_m}"

    if format == "full":
        result = f"{hours} {f_h} {minutes} {f_m}"
        if with_sec:
            result += f" {seconds} {f_s}"
        return result


def to_time(time: int, format: str = 'h') -> int:
    if format == 'h':
        return time // 3600
    elif format == 'm':
        return (time % 3600) // 60
    else:
        logger.error("Неверный аргумент времени")


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


def time_for_qt(time: int) -> QTime:
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)

    return QTime(hours, minutes)