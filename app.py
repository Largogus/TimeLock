from PySide6.QtWidgets import QApplication
from core.system.config import FONT_FAMILY
from pathlib import Path
from UI import main_window
from sys import argv, exit
from loguru import logger
from core.signals.tracker_signals import signal

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.add(LOG_DIR / 'log_{time:YYYY-MM-DD}.log',
           rotation="1 day",
           retention="1 weeks",
           backtrace=True,
           diagnose=True,
           )


def main():
    from core.db.init_db import init_db
    from core.db.session import SessionLocal
    from core.thread.main.tracker import TrackerThread

    init_db()

    app = QApplication(argv)

    font = app.font()
    font.setFamily(FONT_FAMILY)
    app.setFont(font)

    window = main_window.MainWindow()
    window.show()

    tracker = TrackerThread(SessionLocal)

    # tracker.sessionUpdate.connect(lambda app_name: print(get_total_pc_time_today(SessionLocal())))
    signal.errorOccurred.connect(lambda error: logger.error(error))

    tracker.start()

    logger.success("Приложение запустилось")

    app.aboutToQuit.connect(tracker.stop)

    exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Критическая ошибка при запуске приложения")
        raise # Только тесты