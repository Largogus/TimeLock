from core.command.settings import set_settings
from core.db.session import SessionLocal
from core.widgets.thread_manager import thread_manager


def clean_exit(overlays, modal):
    thread_manager.stop_all()

    if modal and modal.isVisible():
        modal.close()

    for ov in overlays:
        if ov.isVisible():
            ov.close()

    with SessionLocal() as s:
        set_settings(s, "focus", 0, int)