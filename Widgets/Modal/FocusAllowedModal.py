from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QLabel, QSizePolicy, QCompleter, QHBoxLayout
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, QSortFilterProxyModel

from Style.PopupStyle import PopupStyle
from Widgets.Buttons.Button import Button
from Widgets.Line import Line
from Widgets.ComboBoxes.PopUp import PopUp
from Widgets.TextsEdits.TextEdit import TextEdit
from core.command.category_command import get_category
from core.command.focus_command import is_focus_allowed, set_focus_allowed
from core.command.get_all_app import get_all_app, get_all_app_with_category
from core.system.desktop import DesktopSize
from core.system.config import FONT_FAMILY
from core.db.session import SessionLocal


class FocusAllowedModal(QWidget):
    def __init__(self):
        super().__init__()
        self.db_session = SessionLocal()

        font = QFont(FONT_FAMILY, 14)
        font.setBold(True)

        self.setFont(font)
        self.setWindowTitle("Разрешённые приложения")
        self.setWindowIcon(QIcon(":src/icon.png"))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.resize(500, 500)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#c4c4c4"))
        palette.setColor(QPalette.ColorRole.Text, QColor("black"))

        x, y = DesktopSize(self)

        self.move(x, y)

        self.raise_()

        layout = QVBoxLayout()

        self.apps = get_all_app(self.db_session, is_id=True)

        label = QLabel()
        label.setText("Разрешённые приложения")

        self.category = PopUp("Категории:")

        self.category.addItems(get_category(self.db_session))
        self.category.currentTextChanged.connect(lambda: self.changeCategoty(self.category.currentText()))
        self.category.close.connect(lambda: self.changeCategoty(" "))

        proxy = QSortFilterProxyModel()

        search = TextEdit(image=":src/icon/search.svg", placeholder="Найти приложение...", ratio=0.40)
        search.setMinimumWidth(250)
        search.setFixedHeight(40)
        search.textChanged.connect(proxy.setFilterFixedString)
        search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        completer_app = [name for name, id in self.apps]
        completer = QCompleter(completer_app)
        completer.setWidget(search)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        popup = completer.popup()
        popup.setAutoFillBackground(False)
        popup.setItemDelegate(PopupStyle(bg=QColor("#e0e0e0"), hbg=QColor(166, 217, 166, 255), clc_bg=QColor("#b4e9b4"),
                                         text_color=QColor("black")))

        search.setCompleter(completer)

        hlay = QHBoxLayout()

        hlay.addWidget(self.category)
        hlay.addWidget(search)

        view = QListView()
        self.model = QStandardItemModel()

        self.setAutoFillBackground(True)
        view.setAutoFillBackground(True)

        self.allowed_list = is_focus_allowed(self.db_session)

        self.setData(self.allowed_list)

        self.model.itemChanged.connect(self.checkbox_changed)

        view.setPalette(palette)

        proxy.setSourceModel(self.model)
        proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        proxy.setFilterKeyColumn(0)

        view.setModel(proxy)
        view.show()

        self.exit = Button("Выйти", align=Qt.AlignmentFlag.AlignCenter, maxs=1920)
        self.exit.clicked.connect(self.hide)

        self.exit.setBackgroundColor(QColor("#8fefae"))
        self.exit.setBackgroundHover(QColor("#7eeda1"))
        self.exit.setBackgroundPressed(QColor("#baf8cd"))

        layout.addWidget(label)
        layout.addWidget(Line("H"))
        layout.addLayout(hlay)
        layout.addWidget(view)
        layout.addWidget(self.exit)

        self.setPalette(palette)
        self.setLayout(layout)

    def checkbox_changed(self, item: QStandardItem):
        app_id = item.data(Qt.ItemDataRole.UserRole)
        if app_id is not None:
            set_focus_allowed(self.db_session, app_id)
            self.allowed_list = is_focus_allowed(self.db_session)
            self.setData(self.allowed_list)

    def setData(self, allowed_list):
        self.model.clear()

        if allowed_list is None:
            allowed_list = []

        for name, id in self.apps:
            item = QStandardItem(name)
            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(id, Qt.ItemDataRole.UserRole)

            if id in allowed_list:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

            self.model.appendRow(item)

    def changeCategoty(self, category):
        if category == " ":
            self.apps = get_all_app(self.db_session, is_id=True)
        else:
            self.apps = get_all_app_with_category(self.db_session, category=category, is_id=True)

        self.setData(self.allowed_list)