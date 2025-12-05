import win32api
from win32gui import GetWindowText, IsWindowVisible, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import Process, NoSuchProcess
from ctypes import windll, create_string_buffer, c_void_p, c_uint, byref, c_ushort, cast, wstring_at, POINTER


SYSTEM_PROCESS = ['explorer.exe',
                  'ApplicationFrameHost.exe',
                  "TextInputHost.exe",
                  "systemsettings.exe",
                  'calculatorapp.exe'
                  ]


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


def get_application():
    apps = {}

    def callback(hwnd, _):
        if IsWindowVisible(hwnd):

            title = GetWindowText(hwnd).lower()

            if title:

                _, pid = GetWindowThreadProcessId(hwnd)

                try:
                    proc = Process(pid)

                    if proc.name() not in SYSTEM_PROCESS:
                        apps[proc.name().lower()] = get_file_name(proc.exe()) or proc.name()[:-4]

                except NoSuchProcess:
                    pass

        return True

    EnumWindows(callback, None)
    return apps


print(get_application())