from PySide6.QtGui import Qt, QColor, QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QTableView, QHeaderView, QMenu, \
    QMessageBox
from Widgets.Buttons.Button import Button
from Widgets.Frame import BaseFrame
from Widgets.Modal.CategoryModal import CategoryModal
from Widgets.ComboBoxes.PopUp import PopUp
from Style.TableStyle import TableDelegate
from Style.MenuStyle import MenuStyle
from Widgets.TextsEdits.TextEdit import TextEdit
from Widgets.Wrapper import Wrapper
from core.command.block_app import add_block_app, is_blocked
from core.command.category_command import get_category
from core.dataset.roles import IdRole
from core.db.session import SessionLocal
from core.statistic.middle_time import get_middle_time
from core.thread.table.table_data_loader import TableDataLoader
from core.widgets.sort_table import SortFilter
from core.widgets.abstract_model_table import TableModel
from Widgets.Panels.AppPanel import AppPanel
from core.signals.table_signals import signal
from core.signals.change_signals import signal_change
from loguru import logger

from core.widgets.thread_manager import thread_manager


class Applications(QWidget):
    def __init__(self):
        super().__init__()
        self.db_session = SessionLocal()

        self.appPanel = AppPanel(self)

        layout = QVBoxLayout()
        layout.addSpacing(-20)

        self.main = BaseFrame(QVBoxLayout())
        self.main.mainLayout.setContentsMargins(20, 20, 20, 0)
        self.main.setBorderRadius(0)

        title = QLabel()
        title_font = title.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setPalette(QPalette(QColor(255, 255, 255)))
        title.setText('Приложения')

        info_window = QLabel()
        info_window.setText("Управление по программам")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        '''----------------------------------'''

        self.proxy_table = SortFilter()

        header = BaseFrame()
        header.setBackgroundColor(QColor("#FFFFFF"))
        header.setMinimumWidth(1000)
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_header = []

        self.category = PopUp("Категории:")

        self.category.addItems(get_category(self.db_session))
        self.category.currentTextChanged.connect(lambda: self.proxy_table.updateCategory(self.category.currentText()))
        self.category.close.connect(lambda: self.proxy_table.updateCategory(""))

        button_header.append(self.category)

        search = TextEdit(image="src/icon/search.svg", placeholder="Найти приложение...", ratio=0.40)
        search.setMinimumWidth(250)
        search.textChanged.connect(lambda: self.proxy_table.updateName(search.text()))
        search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_header.append(search)

        group_button = QHBoxLayout()
        all_btn = Button("Все", maxs=50, min=50, align=Qt.AlignmentFlag.AlignCenter)
        all_btn.clicked.connect(lambda: self.proxy_table.updateLimit(""))

        without_limit_btn = Button("Без лимита", maxs=500, min=100, align=Qt.AlignmentFlag.AlignCenter)
        without_limit_btn.clicked.connect(lambda: self.proxy_table.updateLimit("Нет"))

        with_limit_btn = Button("С лимитом", maxs=50, min=100, align=Qt.AlignmentFlag.AlignCenter)
        with_limit_btn.clicked.connect(lambda: self.proxy_table.updateLimit("С лимитом"))

        group_button.addWidget(all_btn)
        group_button.addWidget(without_limit_btn)
        group_button.addWidget(with_limit_btn)
        group_button.addStretch(1)

        button_header.append(group_button)

        self.filter_search = PopUp("Сортировка:", fixed_width=200)
        self.filter_search.addItems(["По времени", "По алфавиту", "По лимиту", ])
        self.filter_search.currentTextChanged.connect(self.filter_allow)
        self.filter_search.close.connect(self.filter_allow)
        button_header.append(self.filter_search)

        self.table_loader = thread_manager.register(TableDataLoader(SessionLocal))

        self.table = QTableView()
        self.table.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.model = TableModel()
        self.model.dataChanged.connect(self.updAppPanelTime)

        signal.objectCategoryChanged.connect(self.model.updateCategoryInTable)

        self.table.clicked.connect(self.openAppPanel)

        self.proxy_table.setSourceModel(self.model)

        self.table.setModel(self.proxy_table)
        self.table.setMinimumHeight(425)
        self.table.horizontalHeader().setFixedHeight(40)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionsMovable(False)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 350)

        self.delegate_table = TableDelegate(self)
        self.table.setItemDelegateForColumn(5, self.delegate_table)
        self.delegate_table.click_btn.connect(self.small_menu)

        self.table.setAutoFillBackground(True)
        palette = self.table.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(222, 222, 222, 180))
        palette.setColor(QPalette.ColorRole.Button, QColor('#bac8b6'))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor('#000000'))
        palette.setColor(QPalette.ColorRole.Text, QColor('#000000'))
        palette.setColor(QPalette.ColorRole.WindowText, QColor('#000000'))
        self.table.setPalette(palette)
        self.table.setBackgroundRole(QPalette.ColorRole.Base)

        self.table.setMinimumWidth(1000)

        # Более современный вид заголовка
        header_t = self.table.horizontalHeader()
        header_t.setHighlightSections(False)
        header_t.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        self.table_loader.statsReady.connect(lambda data: self.model.update_data(data))

        self.table_loader.start()

        self.main.addElement(title)
        self.main.addElement(info_window)

        for btn in button_header:
            if isinstance(btn, QWidget):
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                header.addElement(btn)
                header.setFixedHeight(60)
            else:
                header.addLayout(btn)

        header.mainLayout.addStretch(2)
        header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.main.addLayout(Wrapper(header))

        self.main.addElement(self.table)

        self.main.mainLayout.addSpacing(50)

        self.appPanel.raise_()

        layout.addWidget(self.main)
        layout.addSpacing(-20)

        self.setLayout(layout)

        signal_change.application_arg.connect(self.category_from_card)

    def category_from_card(self, data):
        self.category.setCurrentText(data)

    def filter_allow(self):
        arg = self.filter_search.currentText()
        if arg == "По времени":
            self.proxy_table.sort(2, Qt.SortOrder.DescendingOrder)
        elif arg == "По лимиту":
            self.proxy_table.sort(3, Qt.SortOrder.DescendingOrder)
        elif arg == "По алфавиту":
            self.proxy_table.sort(0, Qt.SortOrder.DescendingOrder)
        else:
            self.proxy_table.sort(-1, Qt.SortOrder.AscendingOrder)

    def small_menu(self, index):
        menu = QMenu(self)

        cat_modal = CategoryModal(index.data(Qt.ItemDataRole.UserRole))

        data = index.data(Qt.ItemDataRole.UserRole)
        id = index.data(IdRole)

        change_category_action = menu.addAction("Изменить категорию")
        change_limit_menu = menu.addAction("Установить / изменить лимит")

        state = is_blocked(data, SessionLocal(), app_is_name=True)

        if state:
            block_app = menu.addAction("Разблокировать приложение")
        else:
            block_app = menu.addAction("Заблокировать приложение")

        delete_app = menu.addAction("Не отслеживать приложение")

        change_category_action.triggered.connect(lambda: cat_modal.show())
        change_limit_menu.triggered.connect(lambda: signal_change.limit_screen.emit(2, data, "app"))

        def on_delete():
            logger.debug(f"{data} {id}")
            from core.command.dont_tracking import dont_tracking
            from Widgets.Modal.MessageTemplate import MessageTemplate
            modal = MessageTemplate(
                msg_icon=QMessageBox.Icon.Question,
                text=f"Вы уверены, что хотите перестать отслеживать {data}",
                title="Оповещение", standard_btn=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if modal:
                dont_tracking(self.db_session, id)

        def on_blocked():
            from Widgets.Modal.MessageTemplate import MessageTemplate
            modal = MessageTemplate(
                msg_icon=QMessageBox.Icon.Question,
                text=f"Вы уверены, что хотите заблокировать {data}?",
                title="Оповещение", standard_btn=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if modal:
                db_session = SessionLocal()
                add_block_app(data, db_session)

        delete_app.triggered.connect(on_delete)
        block_app.triggered.connect(on_blocked)

        rect = self.table.visualRect(index)
        pos = self.table.viewport().mapToGlobal(rect.bottomLeft())

        menu.setStyle(MenuStyle())

        menu.exec(pos)

    def openAppPanel(self, index):
        model = index.model()
        row = index.row()

        data = {}

        for inx, col in enumerate(range(model.columnCount())):
            info = model.index(row, col).data()
            app_id = model.index(row, col).data(Qt.ItemDataRole.UserRole)
            id = model.index(row, col).data(IdRole)

            if inx == 0: data['name'] = info
            if inx == 1: data['category'] = info
            if inx == 2: data['today'] = info
            if inx == 3: data['limit'] = info

            if col != 5:
                data['middle_time'] = get_middle_time(self.table_loader.db_session_factory, app_id)

            data['id'] = id

        self.appPanel.reopen(data, self.appPanel.setDate)

    def updAppPanelTime(self, index):
        model = index.model()
        row = index.row()

        data = {}

        for inx, col in enumerate(range(model.columnCount())):
            info = model.index(row, col).data()
            app_id = model.index(row, col).data(Qt.ItemDataRole.UserRole)
            id = model.index(row, col).data(IdRole)

            if inx == 0: data['name'] = info
            if inx == 1: data['category'] = info
            if inx == 2: data['today'] = info
            if inx == 3: data['limit'] = info

            if col != 5:
                data['middle_time'] = get_middle_time(self.table_loader.db_session_factory, app_id)

            data['id'] = id

        self.appPanel.setDate(data)

    def resizeEvent(self, event):
        self.appPanel.upd()
        super().resizeEvent(event)