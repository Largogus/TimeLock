import sys

from core.db.db_writer import db_writer
from core.system.app_cache import app_cache
from core.system.localServer import start_local_server, send_raise_signal
from core.system.mutex import single_instance
from os import getenv
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox
from Widgets.Modal.CloseModal.BlockedUser import BlockedUser
from Widgets.Modal.CloseModal.LimitClose import LimitModal
from Widgets.Modal.CloseModal.PClose import PCModal
from Widgets.Overlay import Overlay
from core.command.modal import on_modal_closed, on_modal_rollup, on_pc_closed, on_pc_disabled, on_modal_unblock
from core.signals.core_events import core_events
from core.signals.ui_events import ui_events
from core.system.clean_exit import clean_exit
from pathlib import Path
from UI import main_window
from sys import argv, exit
from loguru import logger
from core.signals.tracker_signals import signal
from core.system.connect_notifications import connect_notifications
from core.system.register import register_command
from core.widgets.notification_manager import NotificationManager
from core.widgets.thread_manager import thread_manager


LOG_DIR = Path(getenv("APPDATA")) / "TimeLock" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(LOG_DIR / 'log_{time:YYYY-MM-DD}.log',
           rotation="1 day",
           retention="1 weeks",
           backtrace=True,
           diagnose=True,
           compression="zip"
           )

_overlay = []
_modal = None
_defer_time = 0
_defer_used = {}
_block_until = {}
app_thread = None


def main():
    global app_thread
    from core.db.init_db import init_db
    from core.db.session import SessionLocal
    from core.thread.main.tracker import TrackerThread
    from core.system.config import FONT_FAMILY
    from core.system.config import SETTINGS, refresh_settings

    if not single_instance.acquire():
        send_raise_signal()
        sys.exit(0)

    init_db()

    refresh_settings()

    app = QApplication(argv)

    styles = QStyleFactory.keys()

    if "windows11" in styles:
        app.setStyle("windows11")
    else:
        app.setStyle("windowsvista")
        logger.info("Стиль windows11 не найден")

    font = app.font()
    font.setFamily(FONT_FAMILY)
    app.setFont(font)

    window = main_window.MainWindow()

    start_local_server(window)

    if not SETTINGS.get("in_tray", 0):
        window.show()

    register_command()

    core_events.register_signal.connect(register_command)

    db_writer.start()
    thread_manager.register_db_writer(db_writer)

    tracker = thread_manager.register(TrackerThread(SessionLocal))

    app_thread = SessionLocal()

    app_cache.session_factory = SessionLocal
    app_cache.load_all()

    signal.errorOccurred.connect(lambda error: logger.error(error))
    ui_events.show_limit_modal.connect(show_limit)
    ui_events.show_limit_pc.connect(lambda: show_limit_pc(app_thread))
    ui_events.show_blocked_user_modal.connect(lambda name, hwnd: show_block(name, hwnd))

    manager = NotificationManager()
    connect_notifications(manager)
    core_events.show_visible.connect(lambda: connect_notifications(manager))

    tracker.start()

    logger.success("Приложение запустилось")

    app.aboutToQuit.connect(lambda: clean_exit(_overlay, _modal))

    try:
        exit(app.exec())
    finally:
        thread_manager.stop_all()
        single_instance.release()


def show_limit(name, hwnd):
    global _modal, _overlay, _defer_used, _block_until

    if name in _block_until:
        _block_until[name] += 1

        if _block_until[name] < 30: # потом заменить на 5*60
            return
        else:
            del _block_until[name]

    ui_events.blockSignals(True)

    is_deferred = _defer_used.get(name, False)

    app = QApplication.instance()
    screens = app.screens()

    _overlay = [Overlay(screen.geometry()) for screen in screens]

    _modal = LimitModal(name, is_deferred)
    _modal.setParent(_overlay[0])
    _modal.btn.clicked.connect(lambda: on_modal_closed(hwnd, _modal, _overlay))
    _modal.btn_rollup.clicked.connect(lambda: on_modal_rollup(hwnd, _modal, _overlay))

    if is_deferred:
        _modal.btn_defer.hide()
    else:
        _modal.btn_defer.clicked.connect(lambda: defer(name))

    _modal.show()


def show_block(name, hwnd):
    global _modal, _overlay, app_thread

    ui_events.blockSignals(True)

    app = QApplication.instance()
    screens = app.screens()

    _overlay = [Overlay(screen.geometry()) for screen in screens]

    _modal = BlockedUser(name, 0)
    _modal.setParent(_overlay[0])
    _modal.btn.clicked.connect(lambda: on_modal_closed(hwnd, _modal, _overlay))
    _modal.btn_rollup.clicked.connect(lambda: on_modal_rollup(hwnd, _modal, _overlay))
    _modal.btn_unblock.clicked.connect(lambda: on_modal_unblock(app_thread, name, _modal, _overlay))

    _modal.show()


def show_limit_pc(db_session):
    global _modal, _overlay, _defer_used, _block_until

    if "pc" in _block_until:
        _block_until["pc"] += 1

        if _block_until["pc"] < 5*60:
            return
        else:
            del _block_until["pc"]

    ui_events.blockSignals(True)

    is_deferred = _defer_used.get("pc", False)

    app = QApplication.instance()
    screens = app.screens()

    _overlay = [Overlay(screen.geometry()) for screen in screens]

    _modal = PCModal(is_deferred)
    _modal.setParent(_overlay[0])
    _modal.btn.clicked.connect(on_pc_closed)

    _modal.btn_disabled.clicked.connect(lambda: on_pc_disabled(db_session, _modal, _overlay))

    if is_deferred:
        _modal.btn_defer.hide()
    else:
        _modal.btn_defer.clicked.connect(lambda: defer("pc"))

    _modal.show()


def defer(name):
    global _overlay, _defer_used

    _defer_used[name] = True
    _block_until[name] = 0
    ui_events.blockSignals(False)

    for ov in _overlay:
        ov.close()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        from Widgets.Modal.MessageTemplate import MessageTemplate

        thread_manager.stop_all()

        MessageTemplate(QMessageBox.Icon.Critical, "Критическая ошибка при запуске приложения", "TimeLock", )
        logger.exception("Критическая ошибка при запуске приложения")