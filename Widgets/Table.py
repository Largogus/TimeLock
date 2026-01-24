from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, Qt
from Widgets.TableItem import TableItem
from core.models.models import App, Blacklist
from core.db.session import SessionLocal
from sqlalchemy import exists, select
import os


class Table(QScrollArea):
    def __init__(self):
        super().__init__()

        self.BACKGROUND_COLOR = QColor('#CFCFCF')
        self.RADIUS = 10

        self.setMinimumHeight(190)

        container = QWidget()
        layout = QVBoxLayout(container)

        with SessionLocal() as s:
            apps = s.query(App).filter(~exists(select(1).where(Blacklist.app_id == App.id))).all()

        for app in apps:
            title = app.name
            path = app.path or "./path"
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