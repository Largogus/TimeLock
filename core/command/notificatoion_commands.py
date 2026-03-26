from PySide6.QtCore import QTimer
from loguru import logger
from win32gui import ShowWindow, SetForegroundWindow, GetForegroundWindow, GetWindow, IsWindow, IsWindowVisible, IsIconic, GetWindowText
from win32con import SW_MINIMIZE, KEYEVENTF_KEYUP, GW_HWNDNEXT, VK_MENU
from win32api import keybd_event


def on_focus_rollup():
    try:
        target = GetForegroundWindow()

        next_hwnd = _get_next_valid_window(target)

        ShowWindow(target, SW_MINIMIZE)

        if next_hwnd:
            fake_alt_press()
            SetForegroundWindow(next_hwnd)
    except Exception:
        logger.exception("Ошибка при безопасном сворачивании")


def fake_alt_press():
    keybd_event(VK_MENU, 0, 0, 0)
    keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)


def _get_next_valid_window(hwnd):
    next_hwnd = GetWindow(hwnd, GW_HWNDNEXT)

    while next_hwnd:
        if _is_valid_window(next_hwnd):
            return next_hwnd
        next_hwnd = GetWindow(next_hwnd, GW_HWNDNEXT)

    return None


def _is_valid_window(hwnd):
    if not hwnd:
        return False
    if not IsWindow(hwnd):
        return False
    if not IsWindowVisible(hwnd):
        return False
    if IsIconic(hwnd):
        return False

    title = GetWindowText(hwnd)
    if not title:
        return False

    return True


def get_next_window(hwnd):
    return GetWindow(hwnd, GW_HWNDNEXT)