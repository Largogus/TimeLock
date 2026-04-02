from sys import executable, argv
from os import execl

from core.system.mutex import single_instance


def restart_app():
    single_instance.release()

    python = executable
    execl(python, python, *argv)