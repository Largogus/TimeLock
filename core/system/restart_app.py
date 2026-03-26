from sys import executable, argv
from os import execl


def restart_app():
    python = executable
    execl(python, python, *argv)