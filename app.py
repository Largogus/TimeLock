from PySide6.QtWidgets import QApplication
from UI import MainWindow
from sys import argv, exit


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow.MainWindow()
    window.show()
    exit(app.exec())