from json import load
from pathlib import Path
from loguru import logger

from core.signals.core_events import core_events

CONFIG_PATH = Path("storage/config.json")
ICON_PATH = Path("src/icon.png")


def load_config() -> dict:
    try:
        with open(CONFIG_PATH, encoding='UTF-8') as f:
            config = load(f)
    except FileNotFoundError:
        logger.exception(f"Конфиг {CONFIG_PATH} не найден")
        raise
    except Exception:
        logger.exception(f"Ошибка при чтении конфига {CONFIG_PATH}")
        raise

    validate_config(config)
    validate_path(ICON_PATH)
    return config


def validate_config(config):
    required_keys = ["first_start",
                     "database_url",
                     "system_process",
                     "friendly_process",
                     "ui"]

    for key in required_keys:
        if key not in config:
            raise KeyError(f"В конфиге отсутствует ключ: '{key}'")

    if not isinstance(config["ui"], dict):
        raise TypeError("'ui' должен быть словарём")
    if not isinstance(config["system_process"], list):
        raise TypeError("'system_process' должен быть списком")
    if not isinstance(config["friendly_process"], dict):
        raise TypeError("'friendly_process' должен быть словарём")

    return True


def validate_path(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Файл {path} не найден")

    return True


def get_settings():
    from core.system.load_settings import load_settings

    return load_settings(DEFAULT_SETTINGS)


def refresh_settings():
    global SETTINGS
    new_settings = get_settings()
    SETTINGS.clear()
    SETTINGS.update(new_settings)


_config = load_config()

DATABASE_PATH = _config['database_url']

SYSTEM_PROCESS = _config['system_process']

FRIENDLY_PROCESS = _config['friendly_process']

FONT_FAMILY = _config["ui"]["font_family"]

DEFAULT_SETTINGS = _config["default_settings"]

ICON_PATH = str(ICON_PATH)

SETTINGS = get_settings()

core_events.settings_edited.connect(refresh_settings)


__all__ = (
    "DATABASE_PATH",
    "SYSTEM_PROCESS",
    'FRIENDLY_PROCESS',
    "FONT_FAMILY",
    "ICON_PATH",
    "SETTINGS"
)