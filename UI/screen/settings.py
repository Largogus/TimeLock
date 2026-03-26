from PySide6.QtGui import QColor, QPalette, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QMessageBox, QFileDialog

from Widgets.Buttons.Button import Button
from Widgets.ComboBoxes.ChoicePopup import ChoicePopup
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from Widgets.Modal.CategoryManager import CategoryManager
from Widgets.Modal.ExceptionManager import ExceptionManager
from core.command.settings import set_settings
from core.db.session import SessionLocal
from core.system.config import SETTINGS
from core.system.delete_all_info import delete_all_info
from core.system.export_stat import export_statistics
from core.system.restart_app import restart_app


class Settings(QWidget):
    def __init__(self):
        super().__init__()

        self.db_session = SessionLocal()

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
        title.setText('Настройки')

        info_window = QLabel()
        info_window.setText("Изменение компонентов работы программы")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        self.main.addElement(title)
        self.main.addElement(info_window)

        self.main.addElement(Line('H'))

        '''|---------------------------------------------|'''

        self.common_block = BaseFrame(QVBoxLayout())
        self.common_block.setBackgroundColor(QColor("#e3e3e3"))

        self.title_common_block = QLabel()
        self.title_common_block.setText("Общие")

        self.label_font = self.title_common_block.font()
        self.label_font.setPointSize(16)
        self.label_font.setBold(True)

        self.mini_label_font = self.title_common_block.font()
        self.mini_label_font.setPointSize(14)
        self.mini_label_font.setBold(True)

        self.label_palette = self.title_common_block.palette()
        self.label_palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.label_palette.setColor(QPalette.ColorRole.Text, QColor("black"))

        self.title_common_block.setFont(self.label_font)
        self.title_common_block.setPalette(self.label_palette)

        self.check_start_app_with_run = QCheckBox()
        self.check_start_app_with_run.setCheckState(Qt.CheckState.Checked)
        self.check_start_app_with_run.setText("Запускать приложение при старте системы")
        self.check_start_app_with_run.setPalette(self.label_palette)
        self.check_start_app_with_run.setFont(self.mini_label_font)

        self.check_start_app_in_tray = QCheckBox()
        self.check_start_app_in_tray.setCheckState(Qt.CheckState.Checked)
        self.check_start_app_in_tray.setText("Запускать свернутым в трей")
        self.check_start_app_in_tray.setPalette(self.label_palette)
        self.check_start_app_in_tray.setFont(self.mini_label_font)

        self.check_show_notification = QCheckBox()
        self.check_show_notification.setCheckState(Qt.CheckState.Checked)
        self.check_show_notification.setText("Показывать уведомления")
        self.check_show_notification.setPalette(self.label_palette)
        self.check_show_notification.setFont(self.mini_label_font)

        self.common_block.addElement(self.title_common_block)
        self.common_block.addElement(self.check_start_app_with_run)
        self.common_block.addElement(self.check_start_app_in_tray)
        self.common_block.addElement(self.check_show_notification)

        self.main.addElement(self.common_block)

        '''|---------------------------------------------|'''

        self.category_and_exception_block = BaseFrame(QVBoxLayout())
        self.category_and_exception_block.setBackgroundColor(QColor("#e3e3e3"))

        self.title_category_and_exception_block = QLabel()
        self.title_category_and_exception_block.setText("Категории и исключения")
        self.title_category_and_exception_block.setFont(self.label_font)
        self.title_category_and_exception_block.setPalette(self.label_palette)

        btn = QHBoxLayout()

        omc = CategoryManager()

        self.button_open_category_manager = Button("Открыть менеджер управления категориями", align=Qt.AlignmentFlag.AlignHCenter)
        self.button_open_category_manager.clicked.connect(lambda: omc.show())

        self.button_open_exception_manager = Button("Открыть менеджер управления исключениями", align=Qt.AlignmentFlag.AlignHCenter)
        self.button_open_exception_manager.clicked.connect(self.open_oem)

        btn.addWidget(self.button_open_category_manager)
        btn.addWidget(self.button_open_exception_manager)

        self.category_and_exception_block.addElement(self.title_category_and_exception_block)
        self.category_and_exception_block.addLayout(btn)

        self.main.addElement(self.category_and_exception_block)

        '''|---------------------------------------------|'''

        self.data_block = BaseFrame(QVBoxLayout())
        self.data_block.setBackgroundColor(QColor("#e3e3e3"))

        self.title_data_block = QLabel()
        self.title_data_block.setText("Данные")
        self.title_data_block.setFont(self.label_font)
        self.title_data_block.setPalette(self.label_palette)

        keep = QHBoxLayout()

        session = QVBoxLayout()

        self.data_session_keep_label = QLabel()
        self.data_session_keep_label.setText("Хранить детальную историю")
        self.data_session_keep_label.setFont(self.mini_label_font)
        self.data_session_keep_label.setPalette(self.label_palette)

        keep_session = SETTINGS.get("keep_session", 1)
        keep_archive = SETTINGS.get("keep_archive", 31)

        self.keep_session_popup = ChoicePopup(fixed_width=350)
        self.keep_session_popup.addItems(["1 день", "1 неделя", "1 месяц"])

        if keep_session == 31: self.keep_session_popup.setCurrentText("1 месяц")
        elif keep_session == 7: self.keep_session_popup.setCurrentText("1 неделя")
        elif keep_session == 1: self.keep_session_popup.setCurrentText("1 день")

        self.keep_session_popup.currentTextChanged.connect(self.updateKeepSession)

        session.addWidget(self.data_session_keep_label)
        session.addWidget(self.keep_session_popup)

        archive = QVBoxLayout()

        self.data_archive_keep_label = QLabel()
        self.data_archive_keep_label.setText("Хранить статистику")
        self.data_archive_keep_label.setFont(self.mini_label_font)
        self.data_archive_keep_label.setPalette(self.label_palette)

        self.keep_archive_popup = ChoicePopup(fixed_width=350)
        self.keep_archive_popup.addItems(["1 месяц", "1 неделя", "1 день"])

        if keep_archive == 31:
            self.keep_archive_popup.setCurrentText("1 месяц")
        elif keep_archive == 7:
            self.keep_archive_popup.setCurrentText("1 неделя")
        elif keep_archive == 1:
            self.keep_archive_popup.setCurrentText("1 день")

        self.keep_archive_popup.currentTextChanged.connect(self.updateKeepArchive)

        archive.addWidget(self.data_archive_keep_label)
        archive.addWidget(self.keep_archive_popup)

        keep.addLayout(session)
        keep.addLayout(archive)

        data_btn = QHBoxLayout()

        self.export = Button("Экспорт статистики", align=Qt.AlignmentFlag.AlignCenter)
        self.export.clicked.connect(self.exportStatistics)

        self.clear_data = Button("Отчистить все данные", align=Qt.AlignmentFlag.AlignCenter)
        self.clear_data.setBackgroundColor(QColor("#ef706b"))
        self.clear_data.setBackgroundHover(QColor("#f0918e"))
        self.clear_data.setBackgroundPressed(QColor("#f16a65"))
        self.clear_data.clicked.connect(self.delete_all_info)

        data_btn.addWidget(self.export)
        data_btn.addWidget(self.clear_data)

        self.data_block.addElement(self.title_data_block)
        self.data_block.addLayout(keep)
        self.data_block.mainLayout.addSpacing(15)
        self.data_block.addLayout(data_btn)

        self.main.addElement(self.data_block)
        self.main.mainLayout.addStretch()

        '''|---------------------------------------------|'''

        layout.addWidget(self.main)
        layout.addSpacing(-20)

        self.setLayout(layout)

    def open_oem(self):
        self.oem = ExceptionManager()
        self.oem.show()
        self.oem.data.emit()

    def updateKeepSession(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        curr = self.keep_session_popup.currentText()
        data = 0

        if curr == "1 день": data = 1
        elif curr == "1 неделя": data = 7
        elif curr == "1 месяц": data = 31

        set_settings(self.db_session, "keep_session", data, int)

        MessageTemplate(title="Оповещение",
                        text="Срок хранения сессий был изменён. Перезапустите приложение,"
                             " чтобы изменения вступили в силу.",
                        msg_icon=QMessageBox().Icon.Information)

    def updateKeepArchive(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        curr = self.keep_archive_popup.currentText()
        data = 0

        if curr == "1 день":
            data = 1
        elif curr == "1 неделя":
            data = 7
        elif curr == "1 месяц":
            data = 31

        set_settings(self.db_session, "keep_archive", data, int)

        MessageTemplate(title="Оповещение",
                        text="Срок хранения архивных записей был изменён. Перезапустите приложение,"
                             " чтобы изменения вступили в силу.",
                        msg_icon=QMessageBox().Icon.Information)

    def exportStatistics(self):
        data = export_statistics(self.db_session)

        path, _ = QFileDialog.getSaveFileName(
            None,
            "Сохранить статистику",
            "statistics.zip",
            "Zip archive (*.zip)"
        )

        if path:
            with open(path, "wb") as f:
                f.write(data.read())

    def delete_all_info(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate
        modal = MessageTemplate(
            msg_icon=QMessageBox.Icon.Warning,
            text=f"Это действие удалит ВСЮ информацию приложения. Вы точно уверены?",
            title="Оповещение", standard_btn=QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        )

        if modal:
            state, msg = delete_all_info(self.db_session)

            MessageTemplate(
                msg_icon=QMessageBox.Icon.Information if state else QMessageBox.Icon.Critical,
                text=f"{msg}. Приложение будет перезапущенно",
                title="Оповещение"
            )

            restart_app()