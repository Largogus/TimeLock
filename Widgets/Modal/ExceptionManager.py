from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QMenu, QMessageBox, QCompleter

from Style.PopupStyle import PopupStyle
from Widgets.TextsEdits.LineEdit import LineEdit
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QAction
from PySide6.QtCore import Qt, Signal
from Widgets.Buttons.Button import Button
from Widgets.Line import Line
from core.command.get_all_app import get_ignored_app, get_all_app
from core.system.desktop import DesktopSize
from core.system.config import FONT_FAMILY, ICON_PATH
from core.db.session import SessionLocal
from core.widgets.manager_exception import delete_exception, add_exception


class ExceptionManager(QWidget):
    data = Signal()

    def __init__(self):
        super().__init__()

        self.db_session = SessionLocal()

        font = QFont(FONT_FAMILY, 14)
        font.setBold(True)

        self.setFont(font)
        self.setWindowTitle("Менеджер управления исключениями")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        lay = QVBoxLayout()

        x, y = DesktopSize(self)

        self.move(x, y)

        self.title = QLabel()
        self.title.setText("Исключённые приложения")

        lay.addWidget(self.title)
        lay.addWidget(Line('H'))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        widget_exception = QWidget()
        widget_exception.setPalette(palette)

        self.lay_widget = QVBoxLayout()

        self.palette_edit = palette
        self.palette_edit.setColor(QPalette.ColorRole.Base, QColor("white"))
        self.palette_edit.setColor(QPalette.ColorRole.Text, QColor("black"))

        widget_exception.setLayout(self.lay_widget)

        scroll.setWidget(widget_exception)

        lay.addWidget(scroll)
        lay.addWidget(Line('H'))

        self.add_exception_name = LineEdit()
        self.add_exception_name.setPlaceholderText("Работа")
        self.add_exception_name.setPalette(self.palette_edit)

        self.apps = get_all_app(self.db_session)

        completer = QCompleter(self.apps)
        completer.setWidget(self.add_exception_name)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        popup = completer.popup()
        popup.setAutoFillBackground(False)
        popup.setItemDelegate(PopupStyle(bg=QColor("#e0e0e0"), hbg=QColor(166, 217, 166, 255), clc_bg=QColor("#b4e9b4"),
                                         text_color=QColor("black")))

        self.add_exception_name.setCompleter(completer)

        add_button = Button("Добавить исключение", align=Qt.AlignmentFlag.AlignCenter, maxs=1920)
        add_button.setBackgroundColor(QColor("#66f092"))
        add_button.setBackgroundHover(QColor("#4dfe85"))
        add_button.setBackgroundPressed(QColor("#67fe97"))

        add_button.clicked.connect(self.add_category)

        lay.addWidget(self.add_exception_name)
        lay.addWidget(add_button)

        self.setPalette(palette)

        self.setLayout(lay)
        self.data.connect(self.setData)
        self.setData()

    def setData(self):
        self.clear_layout(self.lay_widget)
        category_list = get_ignored_app(self.db_session)

        for app in category_list:
            labl = LineEdit()
            labl.setText(app)
            labl.setReadOnly(True)
            labl.setPalette(self.palette_edit)

            action = QAction(QIcon("src/icon/more_vert.svg"), "", labl)
            labl.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

            self.lay_widget.addWidget(labl)

            action.triggered.connect(lambda _, w=labl, a=app: self.open_menu(w, a))

    def tracking(self, exception):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        success, message = delete_exception(self.db_session, exception)

        MessageTemplate(title="Оповещение", text=message,
                        msg_icon=QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

        self.setData()

    def add_category(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        text = self.add_exception_name.text()

        success, message = add_exception(self.db_session, text)

        MessageTemplate(title="Оповещение", text=message,
                        msg_icon=QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

        self.setData()

    def open_menu(self, widget, exception):
        menu = QMenu(self)

        menu.addAction("Начать отслеживать", lambda: self.tracking(exception))

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