from PySide6.QtWidgets import QApplication
from pathlib import Path
from UI import main_window
from sys import argv, exit
from loguru import logger


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.add(LOG_DIR / 'log_{time:YYYY-MM-DD}.log',
           rotation="1 day",
           backtrace=True,
           diagnose=True,
           )


def main():
    from core.db.init_db import init_db

    init_db()

    app = QApplication(argv)
    window = main_window.MainWindow()
    window.show()

    logger.success("Приложение запустилось")
    exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Критическая ошибка при запуске приложения")
        raise # Только тесты