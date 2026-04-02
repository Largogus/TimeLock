from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLineEdit, QMenu


class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        menu.setStyleSheet("""
        QMenu {
            background-color: gray;
            color: white;
        }

        QMenu::item:selected {
            background-color: darkgray;
        }
        """)

        if not self.isReadOnly():
            actions = [
                ("Отменить", self.undo),
                ("Вырезать", self.cut),
                ("Копировать", self.copy),
                ("Вставить", self.paste),
                ("Удалить", self.clear),
                ("Выделить всё", self.selectAll),
            ]
        else:
            actions = [
                ("Копировать", self.copy),
                ("Выделить всё", self.selectAll),
            ]

        for text, slot in actions:
            act = QAction(text, self)
            act.triggered.connect(slot)
            menu.addAction(act)

        menu.exec(event.globalPos())