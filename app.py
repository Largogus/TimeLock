from PySide6.QtWidgets import QApplication
from Widgets.Modal.CloseModal.BlockedUser import BlockedUser
from Widgets.Modal.CloseModal.LimitClose import LimitModal
from Widgets.Modal.CloseModal.PClose import PCModal
from Widgets.Overlay import Overlay
from core.command.modal import on_modal_closed, on_modal_rollup, on_pc_closed, on_pc_disabled, on_modal_unblock
from core.signals.notification_signals import show_notification
from core.signals.ui_events import ui_events
from core.system.clean_exit import clean_exit
from pathlib import Path
from UI import main_window
from sys import argv, exit
from loguru import logger
from core.signals.tracker_signals import signal
from core.widgets.notification_manager import NotificationManager

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

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

    init_db()

    refresh_settings()

    app = QApplication(argv)

    font = app.font()
    font.setFamily(FONT_FAMILY)
    app.setFont(font)

    window = main_window.MainWindow()
    window.show()

    tracker = TrackerThread(SessionLocal)
    app_thread = SessionLocal()

    # tracker.sessionUpdate.connect(lambda app_name: print(get_total_pc_time_today(SessionLocal())))
    signal.errorOccurred.connect(lambda error: logger.error(error))
    ui_events.show_limit_modal.connect(show_limit)
    ui_events.show_limit_pc.connect(lambda: show_limit_pc(app_thread))
    ui_events.show_blocked_user_modal.connect(lambda name, hwnd: show_block(name, hwnd))

    if SETTINGS.get("show_notification", 1):
        manager = NotificationManager(parent=window)

        ui_events.show_focus_notification.connect(
            lambda name, hwnd: manager.show(
                "У вас запущен фокус, %app% свёрнут",
                name,
                hwnd
            )
        )

        show_notification.show_notification_unblocked.connect(
            lambda name: manager.show(
                "%app% разблокирован",
                name
            )
        )

        show_notification.show_notification_blocked.connect(
            lambda name: manager.show(
                "%app% заблокирован",
                name
            )
        )

        show_notification.show_notification_app_not_tracking.connect(
            lambda name: manager.show(
                "%app% больше не отслеживатеся, снова отслеживать можете в Настройки",
                name
            )
        )

        show_notification.show_notification_app_tracking.connect(
            lambda name: manager.show(
                "%app% снова отслеживатеся",
                name
            )
        )

        show_notification.show_notification_error_limit.connect(
            lambda: manager.show(
                "Лимит для ПК не может быть меньше 30 минут"
            )
        )

    tracker.start()

    logger.success("Приложение запустилось")

    app.aboutToQuit.connect(lambda: clean_exit(tracker, _overlay, _modal))

    exit(app.exec())


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

        if _block_until["pc"] < 30: # потом заменить на 5*60
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
        logger.exception("Критическая ошибка при запуске приложения")
        raise # Только тесты!!