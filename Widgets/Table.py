from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, Qt
from Widgets.TableItem import TableItem
from core.json_manager import read
import os


class Table(QScrollArea):
    def __init__(self):
        super().__init__()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_file = os.path.join(project_root, 'storage', 'monitored_app.json')

        self.BACKGROUND_COLOR = QColor('#CFCFCF')
        self.RADIUS = 10

        self.setMinimumHeight(190)

        container = QWidget()
        layout = QVBoxLayout(container)

        json_txt = read(path_file)

        for i in json_txt:
            title = json_txt[i].get('title', "Undefined")
            path = json_txt[i].get('path', "Undefined")
            layout.addWidget(TableItem(self.viewport(), title, path))
            layout.setSpacing(10)

        layout.addStretch()
        self.setWidget(container)
        self.setWidgetResizable(True)

    def paintEvent(self, event):
        paint = QPainter(self.viewport())
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.viewport().rect()

        paint.setBrush(QBrush(self.BACKGROUND_COLOR))
        paint.setPen(Qt.PenStyle.NoPen)

        paint.drawRoundedRect(rect, self.RADIUS, self.RADIUS)