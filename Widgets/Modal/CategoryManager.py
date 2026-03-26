from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QMenu, QMessageBox
from Widgets.TextsEdits.LineEdit import LineEdit
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QAction
from PySide6.QtCore import Qt
from Widgets.Buttons.Button import Button
from Widgets.Line import Line
from Widgets.Buttons.ToolButton import ToolButton
from core.command.category_command import get_category
from core.system.desktop import DesktopSize
from core.system.config import FONT_FAMILY, ICON_PATH
from core.db.session import SessionLocal
from core.widgets.manager_category import delete_category, add_category, change_category


class CategoryManager(QWidget):
    def __init__(self):
        super().__init__()

        font = QFont(FONT_FAMILY, 14)
        font.setBold(True)

        self.db_session = SessionLocal()

        self.setFont(font)
        self.setWindowTitle("Менеджер управления категориями")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        lay = QVBoxLayout()

        x, y = DesktopSize(self)

        self.move(x, y)

        self.title = QLabel()
        self.title.setText("Категории приложений")

        lay.addWidget(self.title)
        lay.addWidget(Line('H'))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        widget_category = QWidget()
        widget_category.setPalette(palette)

        self.lay_widget = QVBoxLayout()

        self.palette_edit = palette
        self.palette_edit.setColor(QPalette.ColorRole.Base, QColor("white"))
        self.palette_edit.setColor(QPalette.ColorRole.Text, QColor("black"))

        widget_category.setLayout(self.lay_widget)

        scroll.setWidget(widget_category)

        lay.addWidget(scroll)
        lay.addWidget(Line('H'))

        self.add_category_name = LineEdit()
        self.add_category_name.setPlaceholderText("Работа")
        self.add_category_name.setPalette(self.palette_edit)

        add_button = Button("Добавить категорию", align=Qt.AlignmentFlag.AlignCenter)
        add_button.setBackgroundColor(QColor("#66f092"))
        add_button.setBackgroundHover(QColor("#4dfe85"))
        add_button.setBackgroundPressed(QColor("#67fe97"))

        add_button.clicked.connect(self.add_category)

        lay.addWidget(self.add_category_name)
        lay.addWidget(add_button)

        self.setPalette(palette)

        self.setLayout(lay)
        self.setData()

    def setData(self):
        category_list = get_category(self.db_session)

        for category in category_list:
            labl = LineEdit()
            labl.setText(category)
            labl.setReadOnly(True)
            labl.setPalette(self.palette_edit)

            action = QAction(QIcon("src/icon/more_vert.svg"), "", labl)
            labl.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

            self.lay_widget.addWidget(labl)

            action.triggered.connect(lambda _, w=labl, c=category: self.open_menu(w, c))

    def delete_category(self, category):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        success, message = delete_category(self.db_session, category)

        MessageTemplate(title="Оповещение", text=message,
                        msg_icon=QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

        self.clear_layout(self.lay_widget)
        self.setData()

    def rename_category(self, widget: LineEdit):
        last_text = widget.text()
        widget.setReadOnly(False)
        widget.setFocus()

        save_btn = ToolButton(
            icon_path="src/icon/done.svg",
            icon_size=16,
            bg_color=QColor(217, 217, 217),
            hover_color=QColor(100, 255, 100, 100),
            parent=widget
        )
        save_btn.show()

        cancel_btn = ToolButton(
            icon_path="src/icon/close.svg",
            icon_size=16,
            bg_color=QColor(217, 217, 217),
            hover_color=QColor(255, 100, 100, 100),
            parent=widget
        )
        cancel_btn.show()

        h = widget.height()
        btn_size = 16
        margin = 16
        cancel_btn.setGeometry(widget.width() - btn_size - margin, (h - btn_size) // 2, btn_size, btn_size + 3)
        save_btn.setGeometry(widget.width() - 2 * btn_size - 2 * margin, (h - btn_size) // 2, btn_size, btn_size + 3)

        def save():
            from Widgets.Modal.MessageTemplate import MessageTemplate
            text = widget.text().strip()
            widget.setReadOnly(True)
            save_btn.deleteLater()
            cancel_btn.deleteLater()
            success, message = change_category(self.db_session, last_text, text)

            MessageTemplate(title="Оповещение", text=message,
                            msg_icon=QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

            self.clear_layout(self.lay_widget)
            self.setData()

        def cancel():
            widget.setReadOnly(True)
            widget.setText(last_text)
            save_btn.deleteLater()
            cancel_btn.deleteLater()
            self.clear_layout(self.lay_widget)
            self.setData()

        save_btn.clicked.connect(save)
        cancel_btn.clicked.connect(cancel)

        old_keyPress = widget.keyPressEvent

        def new_keyPress(event):
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                save()
            elif event.key() == Qt.Key.Key_Escape:
                cancel()
            else:
                old_keyPress(event)

        widget.keyPressEvent = new_keyPress

    def add_category(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        text = self.add_category_name.text()

        success, message = add_category(self.db_session, text)

        MessageTemplate(title="Оповещение", text=message,
                        msg_icon=QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

        self.clear_layout(self.lay_widget)
        self.setData()

    def open_menu(self, widget, category):
        menu = QMenu(self)

        menu.addAction("Переименовать", lambda: self.rename_category(widget))
        menu.addAction("Удалить", lambda: self.delete_category(category))

        pos = widget.mapToGlobal(widget.rect().bottomRight())
        menu.exec(pos)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue

            w = item.widget()
            l = item.layout()
            s = item.spacerItem()

            if w is not None:
                layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
            elif l is not None:
                self.clear_layout(l)
                layout.removeItem(l)
            elif s is not None:
                layout.removeItem(s)