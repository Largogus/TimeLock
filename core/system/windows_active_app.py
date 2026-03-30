from typing import Tuple, Optional
from win32gui import GetWindowText, IsWindowVisible, GetClassName, GetForegroundWindow, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import Process, NoSuchProcess, process_iter, AccessDenied
from core.system.config import SYSTEM_PROCESS, FRIENDLY_PROCESS, SYSTEM_CLASSES, FRIENDLY_UWP
from ctypes import windll, create_string_buffer, c_void_p, c_uint, byref, c_ushort, cast, wstring_at, POINTER, \
    create_unicode_buffer, wintypes
from loguru import logger


def get_active_window_app() -> Tuple[Optional[str], Optional[str], Optional[Process], Optional[int]]:
    try:
        hwnd = GetForegroundWindow()

        if not hwnd or not IsWindowVisible(hwnd):
            return "__IGNORE__", None, None, None

        class_name = GetClassName(hwnd)

        if class_name in SYSTEM_CLASSES:
            return "__IGNORE__", None, None, None

        title = GetWindowText(hwnd)
        if not title or not title.strip():
            return "__IGNORE__", None, None, None

        _, pid = GetWindowThreadProcessId(hwnd)
        proc = Process(pid)

        name_lower = proc.name().lower()

        if name_lower in SYSTEM_PROCESS:
            return "__IGNORE__", None, None, None

        exe_path = proc.exe()

        if name_lower == "applicationframehost.exe":
            return "__IGNORE__", exe_path, proc, hwnd

        if name_lower in ("java.exe", "javaw.exe"):
            title = GetWindowText(hwnd)

            return title, exe_path, proc, hwnd

        if proc.name() in FRIENDLY_PROCESS:
            return FRIENDLY_PROCESS[proc.name()], exe_path, proc, hwnd

        app_name = _get_file_name(exe_path)
        if not app_name:
            title = GetWindowText(hwnd)
            if title and title.strip():
                app_name = title
            else:
                app_name = proc.name().rsplit(".", 1)[0]

        return app_name, exe_path, proc, hwnd
    except Exception:
        return None, None, None, None


def _get_file_name(path: str) -> str | None:     # Вспомнить работу функции
    size = windll.version.GetFileVersionInfoSizeW(path, None)

    if not size:
        return None

    buff = create_string_buffer(size)
    if not windll.version.GetFileVersionInfoW(path, 0, size, buff):
        return None

    lange = c_void_p()
    len = c_uint()

    if not windll.version.VerQueryValueW(buff, r'\VarFileInfo\Translation', byref(lange), byref(len)):
        return None

    array = c_ushort * 2
    lang_codepage = cast(lange, POINTER(array)).contents
    lang, codepage = lang_codepage[0], lang_codepage[1]

    block = fr'\StringFileInfo\{lang:04x}{codepage:04x}\FileDescription'

    de_buff = c_void_p()
    size = c_uint()

    if windll.version.VerQueryValueW(buff, block, byref(de_buff), byref(size)):
        return wstring_at(de_buff)

    return None


def _find_active_uwp(pid):
    hwnds = []

    def callback(h, param):
        if IsWindowVisible(h):
            _, p = GetWindowThreadProcessId(h)
            if p == pid:
                param.append(h)
        return True

    EnumWindows(callback, hwnds)

    for h in hwnds:
        aumid = _get_uwp_aumid(h)
        if aumid:
            return h, aumid

    return None, None


def _get_uwp_aumid(hwnd):
    shell32 = windll.shell32
    shell32.GetApplicationUserModelId.argtypes = [
        wintypes.HWND,
        POINTER(wintypes.ULONG),
        wintypes.LPWSTR
    ]
    shell32.GetApplicationUserModelId.restype = wintypes.HRESULT

    length = wintypes.ULONG(512)
    aumid_buf = create_unicode_buffer(512)

    hr = shell32.GetApplicationUserModelId(hwnd, byref(length), aumid_buf)
    if hr != 0:
        return ""

    value = aumid_buf.value
    if "!" in value:
        value = value.split("!")[0]
    return value


def is_safe_window(hwnd) -> bool:
    try:
        if not hwnd:
            return False

        if not IsWindowVisible(hwnd):
            return False

        class_name = GetClassName(hwnd)

        if class_name in SYSTEM_CLASSES:
            return False

        _, pid = GetWindowThreadProcessId(hwnd)
        proc_name = Process(pid).name().lower()

        if proc_name == "explorer.exe" and class_name.startswith("Shell"):
            return False

        title = GetWindowText(hwnd)
        if not title or not title.strip():
            return False

        return True

    except Exception:
        return False