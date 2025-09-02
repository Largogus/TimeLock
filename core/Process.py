from win32gui import GetWindowText, IsWindowVisible, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import Process, NoSuchProcess


def remove_system_process(apps: dict):
    SYSTEM_PROCESS = ['explorer.exe',
                      'ApplicationFrameHost.exe',
                      "TextInputHost.exe",
                      "systemsettings.exe",
                      'calculatorapp.exe'
                      ]

    for i in SYSTEM_PROCESS:
        apps.pop(i.lower(), None)


def get_application():
    apps = {}

    def callback(hwnd, _):
        if IsWindowVisible(hwnd):

            title = GetWindowText(hwnd).lower()

            if title:

                _, pid = GetWindowThreadProcessId(hwnd)

                try:
                    proc = Process(pid)
                    apps[proc.name().lower()] = proc.name()
                except NoSuchProcess:
                    pass

        return True

    EnumWindows(callback, None)
    remove_system_process(apps)
    return apps