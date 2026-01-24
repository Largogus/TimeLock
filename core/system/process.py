import win32api
from win32gui import GetWindowText, IsWindowVisible, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import Process, NoSuchProcess, process_iter, AccessDenied
from core.system.config import SYSTEM_PROCESS, FRIENDLY_PROCESS
from ctypes import windll, create_string_buffer, c_void_p, c_uint, byref, c_ushort, cast, wstring_at, POINTER
from loguru import logger


def get_file_name(path: str) -> str | None:     # Вспомнить работу функции
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


def get_application() -> dict:
    apps = {}

    def callback(hwnd, _):
        if not IsWindowVisible(hwnd):
            return True

        _, pid = GetWindowThreadProcessId(hwnd)
        try:
            proc = Process(pid)
            name_lower = proc.name().lower()

            if name_lower in SYSTEM_PROCESS:
                return True

            exe_path = proc.exe()

            app_name = None

            if name_lower == "applicationframehost.exe":
                title = GetWindowText(hwnd)
                if title:
                    apps.setdefault(title, exe_path)
                return True

            if name_lower in ("java.exe", "javaw.exe"):
                title = GetWindowText(hwnd)
                if title:
                    apps.setdefault(title, exe_path)
                return True

            if proc.name() in FRIENDLY_PROCESS:
                apps.setdefault(FRIENDLY_PROCESS[proc.name()], exe_path)
                return True

            app_name = get_file_name(exe_path)
            if not app_name:
                title = GetWindowText(hwnd)
                if title and title.strip():
                    app_name = title
                else:
                    app_name = proc.name().rsplit(".", 1)[0]

            apps.setdefault(app_name, exe_path)
        except NoSuchProcess:
            pass

        return True

    EnumWindows(callback, None)
    return apps


print(get_application())