import time
from loguru import logger
from win32api import GetCurrentThreadId
from win32con import SW_RESTORE, HWND_TOPMOST, SWP_NOMOVE, HWND_NOTOPMOST, SWP_NOSIZE
from win32gui import GetForegroundWindow, ShowWindow, SetForegroundWindow, FlashWindow, SetWindowPos
from win32process import GetWindowThreadProcessId, AttachThreadInput


def force_show_window(window):
    if window.isHidden():
        window.show()

    window.showNormal()
    window.raise_()
    window.activateWindow()


def force_foreground(hwnd):
    try:
        fg_window = GetForegroundWindow()

        if fg_window == hwnd:
            return

        current_thread = GetCurrentThreadId()
        fg_thread, _ = GetWindowThreadProcessId(fg_window)

        AttachThreadInput(fg_thread, current_thread, True)

        ShowWindow(hwnd, SW_RESTORE)
        SetForegroundWindow(hwnd)

        AttachThreadInput(fg_thread, current_thread, False)

    except Exception as e:
        logger.error(f"force_foreground error: {e}")


def flash_window(hwnd):
    try:
        FlashWindow(hwnd, True)
    except:
        pass


def bring_to_front(window):
    try:
        hwnd = int(window.winId())

        force_show_window(window)

        ShowWindow(hwnd, SW_RESTORE)
        SetForegroundWindow(hwnd)

        time.sleep(0.05)

        force_foreground(hwnd)

        time.sleep(0.05)

        SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE
        )
        SetWindowPos(
            hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE
        )

        if GetForegroundWindow() != hwnd:
            flash_window(hwnd)

        logger.success("Окно успешно поднято")

    except Exception as e:
        logger.error(f"bring_to_front error: {e}")