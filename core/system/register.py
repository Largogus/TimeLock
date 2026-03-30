from os import path
from winreg import OpenKey, SetValueEx, CloseKey, KEY_SET_VALUE, REG_SZ, HKEY_CURRENT_USER, DeleteValue, QueryValueEx, \
    KEY_READ

from loguru import logger

from core.system.config import SETTINGS


def is_autorun(name: str) -> bool:
    try:
        key = OpenKey(
            HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            KEY_READ
        )
        value, _ = QueryValueEx(key, name)
        CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def add_to_auto_run():
    if is_autorun("TimeLock"):
        return

    exe = path.abspath("TimeLock.exe")

    key = OpenKey(
        HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        KEY_SET_VALUE
    )

    SetValueEx(key, "TimeLock", 0, REG_SZ, exe)
    CloseKey(key)

    logger.debug("Приложение добавленно в автозагрузку")


def remove_to_auto_run():
    if not is_autorun("TimeLock"):
        return

    key = OpenKey(
        HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        KEY_SET_VALUE
    )

    DeleteValue(key, "TimeLock")
    CloseKey(key)

    logger.debug(f"TimeLock удалён из автозагрузки")


def register_command():
    if SETTINGS.get("auto_start", 1):
        add_to_auto_run()
    else:
        remove_to_auto_run()