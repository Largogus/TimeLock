from json import load, dump
from loguru import logger


def read(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = load(f)

        return data
    except FileNotFoundError:
        logger.error('Файл не найден')


def write(path: str, data: dict):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        logger.error('Файл не найден')
    except FileExistsError:
        logger.error('Файл уже существует')