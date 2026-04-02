from win32gui import PostMessage, ShowWindow
from win32con import WM_CLOSE, SW_MINIMIZE, SE_PRIVILEGE_ENABLED, TOKEN_QUERY, TOKEN_ADJUST_PRIVILEGES, EWX_SHUTDOWN, EWX_FORCE
from win32security import LookupPrivilegeValue, OpenProcessToken, AdjustTokenPrivileges
from win32api import GetCurrentProcess, ExitWindowsEx

from core.command.block_app import remove_block_app
from core.command.settings import set_settings
from core.models.App import App
from core.models.BlockApp import BlockApp
from core.signals.ui_events import ui_events
from loguru import logger


def on_modal_closed(hwnd, modal, overlays):
    if modal:
        modal.close()

    if overlays:
        for overlay in overlays:
            overlay.close()

    try:
        PostMessage(hwnd, WM_CLOSE, 0, 0)
    except Exception:
        logger.exception("Приложение не удалось закрыть")

    ui_events.blockSignals(False)


def on_modal_rollup(hwnd, modal, overlays):
    if modal:
        modal.close()

    if overlays:
        for overlay in overlays:
            overlay.close()

    try:
        ShowWindow(hwnd, SW_MINIMIZE)
    except Exception:
        logger.exception("Приложение не удалось свернуть")

    ui_events.blockSignals(False)


def on_pc_closed():
    hToken = OpenProcessToken(
        GetCurrentProcess(),
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    )

    privilege_id = LookupPrivilegeValue(None, "SeShutdownPrivilege")
    AdjustTokenPrivileges(hToken, False, [(privilege_id, SE_PRIVILEGE_ENABLED)])

    ExitWindowsEx(EWX_SHUTDOWN | EWX_FORCE, 0)


def on_pc_disabled(db_session, modal, overlays):
    if modal:
        modal.close()

    if overlays:
        for overlay in overlays:
            overlay.close()

    set_settings(db_session, "state_limit_pc", 0, int)


def on_modal_unblock(db_session, name, modal, overlays):
        if modal:
            modal.close()

        if overlays:
            for overlay in overlays:
                overlay.close()

        remove_block_app(name, db_session)