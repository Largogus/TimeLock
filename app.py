from PySide6.QtWidgets import QApplication
from UI import MainWindow
from sys import argv, exit
from loguru import logger


logger.add('logs/log_{time:YYYY-MM-DD}')

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow.MainWindow()
    window.show()
    logger.success("Приложение запустилось")
    exit(app.exec())