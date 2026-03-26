from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from core.command.settings import set_settings
from core.db.session import SessionLocal


def clean_exit(tracker, overlays, modal):
    tracker.stop()

    if modal and modal.isVisible():
        modal.close()

    for ov in overlays:
        if ov.isVisible():
            ov.close()

    with SessionLocal() as s:
        set_settings(s, "focus", 0, int)