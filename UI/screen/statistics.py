from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QPalette, Qt, QPainter, QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolTip
from PySide6.QtCharts import QPieSeries, QBarSet, QChart, QChartView, \
    QBarCategoryAxis, QValueAxis, QBarSeries
from Widgets.ComboBoxes.ChoicePopup import ChoicePopup
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from Widgets.Wrapper import Wrapper
from core.db.session import SessionLocal
from core.signals.statistics_signsl import stats_signal
from core.statistic.get_all_stat import get_all_stats
from core.statistic.get_bar_chart_data import get_category_info, get_app_info, get_display_value_and_unit
from core.system.date import normal_time
from core.thread.stat.get_stat_info import StatisticThread


class Statistics(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addSpacing(-20)

        self.db_session = SessionLocal()

        self.main = BaseFrame(QVBoxLayout())
        self.main.mainLayout.setContentsMargins(20, 20, 20, 0)
        self.main.setBorderRadius(0)

        title = QLabel()
        title_font = title.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setPalette(QPalette(QColor(255, 255, 255)))
        title.setText('Статистика')

        info_window = QLabel()
        info_window.setText("Подробная информация по активности в приложениях")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        self.main.addElement(title)
        self.main.addElement(info_window)

        self.main.addElement(Line('H'))

        self.popup_date = ChoicePopup()
        self.popup_date.addItems(["Сегодня", "Неделя", "Месяц"])
        self.popup_date.setMaximumWidth(1920)
        self.popup_date.currentTextChanged.connect(self.setData)

        self.timer = QTimer(self)
        self.timer.setInterval(20000)
        self.timer.timeout.connect(self.setData)
        self.timer.start()

        self.main.addElement(self.popup_date)

        h_layout = QHBoxLayout()

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor("black"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("black"))

        font_size = 16
        bold = True

        daily_stats = BaseFrame(box=QVBoxLayout(), border=14)
        daily_stats.setBackgroundColor(QColor("#FFFFFF"))

        daily_stats_label = QLabel()
        daily_stats_label.setPalette(palette)
        daily_stats_label.setText("График активности")

        daily_stats_label_font = daily_stats_label.font()
        daily_stats_label_font.setBold(bold)
        daily_stats_label_font.setPointSize(font_size)

        daily_stats_label.setFont(daily_stats_label_font)

        h_card = QHBoxLayout()

        daily_stats_card_total = BaseFrame(box=QVBoxLayout(), border=14)
        daily_stats_card_total.setBackgroundColor(QColor("#f0f0f0"))

        daily_stats_time_title = QLabel()
        daily_stats_time_title.setPalette(palette)
        daily_stats_time_title.setText(f"Общее время")
        label_title_font = daily_stats_time_title.font()
        label_title_font.setPointSize(15)
        label_title_font.setBold(True)
        daily_stats_time_title.setFont(label_title_font)

        self.daily_stats_time = QLabel()
        self.daily_stats_time.setPalette(palette)
        label_font = self.daily_stats_time.font()
        label_font.setPointSize(14)
        label_font.setBold(True)
        self.daily_stats_time.setFont(label_font)

        daily_stats_card_total.addElement(daily_stats_time_title, alignment=Qt.AlignmentFlag.AlignCenter)
        daily_stats_card_total.addElement(self.daily_stats_time, alignment=Qt.AlignmentFlag.AlignCenter)

        daily_stats_card_nonfocus = BaseFrame(box=QVBoxLayout(), border=14)
        daily_stats_card_nonfocus.setBackgroundColor(QColor("#f0f0f0"))

        daily_stats_nonfocus_title = QLabel()
        daily_stats_nonfocus_title.setPalette(palette)
        daily_stats_nonfocus_title.setText(f"Без фокуса")
        daily_stats_nonfocus_title.setFont(label_title_font)

        self.daily_stats_nonfocus = QLabel()
        self.daily_stats_nonfocus.setPalette(palette)
        self.daily_stats_nonfocus.setFont(label_font)

        daily_stats_card_nonfocus.addElement(daily_stats_nonfocus_title, alignment=Qt.AlignmentFlag.AlignCenter)
        daily_stats_card_nonfocus.addElement(self.daily_stats_nonfocus, alignment=Qt.AlignmentFlag.AlignCenter)

        daily_stats_card_focus = BaseFrame(box=QVBoxLayout(), border=14)
        daily_stats_card_focus.setBackgroundColor(QColor("#f0f0f0"))

        daily_stats_focus_title = QLabel()
        daily_stats_focus_title.setPalette(palette)
        daily_stats_focus_title.setText(f"С фокусом")
        daily_stats_focus_title.setFont(label_title_font)

        self.daily_stats_focus = QLabel()
        self.daily_stats_focus.setPalette(palette)
        self.daily_stats_focus.setFont(label_font)

        daily_stats_card_focus.addElement(daily_stats_focus_title, alignment=Qt.AlignmentFlag.AlignCenter)
        daily_stats_card_focus.addElement(self.daily_stats_focus, alignment=Qt.AlignmentFlag.AlignCenter)

        daily_stats_card_session = BaseFrame(box=QVBoxLayout(), border=14)
        daily_stats_card_session.setBackgroundColor(QColor("#f0f0f0"))

        self.daily_stats_session_title = QLabel()
        self.daily_stats_session_title.setPalette(palette)
        self.daily_stats_session_title.setFont(label_title_font)

        self.daily_stats_session = QLabel()
        self.daily_stats_session.setPalette(palette)
        self.daily_stats_session.setFont(label_font)

        daily_stats_card_session.addElement(self.daily_stats_session_title, alignment=Qt.AlignmentFlag.AlignCenter)
        daily_stats_card_session.addElement(self.daily_stats_session, alignment=Qt.AlignmentFlag.AlignCenter)

        h_card.addWidget(daily_stats_card_total)
        h_card.addWidget(daily_stats_card_nonfocus)
        h_card.addWidget(daily_stats_card_focus)
        h_card.addWidget(daily_stats_card_session)

        daily_stats.addLayout(Wrapper(daily_stats_label))
        daily_stats.addLayout(h_card)

        '''-----------------------------------------------------------------------'''

        category_stats = BaseFrame(box=QVBoxLayout(), border=14)
        category_stats.setBackgroundColor(QColor("#FFFFFF"))

        category_stats_label = QLabel()
        category_stats_label.setPalette(palette)
        category_stats_label.setText("Топ приложений")

        category_stats_label_font = category_stats_label.font()
        category_stats_label_font.setBold(bold)
        category_stats_label_font.setPointSize(font_size)

        category_stats_label.setFont(category_stats_label_font)

        self.category_stats_chart = QChart()
        self.category_stats_chart.setTitle("Статистика по категориям")

        self.category_axis_y = QValueAxis()
        self.category_axis_y.setTitleText("Минуты")
        self.category_axis_y.setLabelFormat("%i")
        self.category_stats_chart.addAxis(self.category_axis_y, Qt.AlignmentFlag.AlignLeft)

        self.category_stats_axis_x = QBarCategoryAxis()
        self.category_stats_axis_x.setTitleText("Категории")
        self.category_stats_axis_x.setLabelsVisible(False)
        self.category_stats_chart.addAxis(self.category_stats_axis_x, Qt.AlignmentFlag.AlignBottom)

        self.category_stats_series = QBarSeries()
        self.category_stats_chart.addSeries(self.category_stats_series)

        self.category_stats_series.attachAxis(self.category_axis_y)
        self.category_stats_series.attachAxis(self.category_stats_axis_x)

        category_stats_chart_view = QChartView(self.category_stats_chart)
        category_stats_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        category_stats_chart_view.setFixedHeight(250)

        category_stats_chart_view_palette = category_stats_chart_view.palette()
        category_stats_chart_view_palette.setColor(QPalette.ColorRole.Base, QColor('#9ae59b'))
        category_stats_chart_view_palette.setColor(QPalette.ColorRole.Window, QColor('#9ae59b'))

        category_stats_chart_view.setPalette(category_stats_chart_view_palette)

        category_stats.addElement(category_stats_label, alignment=Qt.AlignmentFlag.AlignCenter)
        category_stats.addElement(category_stats_chart_view)

        '''-------------------------------------------------------------------------------------'''

        apps_stats = BaseFrame(box=QVBoxLayout(), border=14)
        apps_stats.setBackgroundColor(QColor("#FFFFFF"))

        apps_stats_label = QLabel()
        apps_stats_label.setPalette(palette)
        apps_stats_label.setText("Топ приложений")

        apps_stats_label_font = apps_stats_label.font()
        apps_stats_label_font.setBold(bold)
        apps_stats_label_font.setPointSize(font_size)

        apps_stats_label.setFont(apps_stats_label_font)

        apps_stats.addElement(apps_stats_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.series = QPieSeries()
        self.series.setHoleSize(0.45)
        self.series.setLabelsVisible(False)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setTitle("Активность по приложениям")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        self.app_stats_chart_view = QChartView(self.chart)
        self.app_stats_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.app_stats_chart_view.setFixedHeight(250)

        self.info_label = QLabel(self)
        self.info_label.raise_()
        self.info_label.setWindowFlags(Qt.WindowType.ToolTip)

        self.info_label.setStyleSheet("""
            background: #333;
            color: white;
            padding: 4px;
            border-radius: 4px;
        """)

        self.info_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.info_label.hide()

        app_stats_chart_view_palette = self.chart.palette()
        app_stats_chart_view_palette.setColor(QPalette.ColorRole.Base, QColor('#9ae59b'))
        app_stats_chart_view_palette.setColor(QPalette.ColorRole.Window, QColor('#9ae59b'))

        self.app_stats_chart_view.setPalette(app_stats_chart_view_palette)

        apps_stats.addElement(self.app_stats_chart_view)

        h_layout.addWidget(category_stats)
        h_layout.addWidget(apps_stats)

        self.main.addElement(daily_stats)
        self.main.addLayout(h_layout)
        self.main.mainLayout.addStretch()

        layout.addWidget(self.main)

        self.setLayout(layout)

        stats_signal.upd_stats.connect(self.setData)
        self.setData()

    def show_tooltip(self, status, bar_set, value, unit):
        if status:
            QToolTip.showText(QCursor.pos(), f"{bar_set.label()}: {value} {unit}")

    def on_slice_hovered(self, state):
        slice_ = self.sender()
        if state:
            slice_.setExploded(True)
            slice_.setBorderWidth(3)

            value = slice_.property("display_value")
            unit = slice_.property("unit")
            text = f"{slice_.label()}: {value} {unit}"

            self.info_label.setText(text)
            self.info_label.adjustSize()
            self.info_label.show()

            cursor_pos = QCursor.pos()
            self.info_label.move(cursor_pos.x() + 15, cursor_pos.y() + 15)

        else:
            slice_.setExploded(False)
            slice_.setBorderWidth(1)
            self.info_label.hide()

    def cursor_on_chart(self):
        pos = self.app_stats_chart_view.mapFromGlobal(QCursor.pos())
        return self.app_stats_chart_view.rect().contains(pos)

    def setData(self):
        if self.cursor_on_chart():
            return

        period = self.popup_date.currentText()

        total_time, time_in_focus, time_without_focus, session_count = get_all_stats(self.db_session, period)
        data_dict = get_category_info(self.db_session, period)
        data_app = get_app_info(self.db_session, period)

        self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)

        self.series.clear()

        period = self.popup_date.currentText()

        self.daily_stats_session_title.setText(f"Сессии за {period.lower()}" if period != "Неделя"
                                               else "Сессии за неделю")

        self.daily_stats_time.setText(f"{normal_time(total_time)}")
        self.daily_stats_nonfocus.setText(f"{normal_time(time_without_focus)}")
        self.daily_stats_focus.setText(f"{normal_time(time_in_focus)}")
        self.daily_stats_session.setText(f"{session_count}")

        sorted_data = sorted(data_app.items(), key=lambda x: x[1][1], reverse=True)[:5]
        other = sorted(data_app.items(), key=lambda x: x[1][1], reverse=True)[5:]

        for app, (display_value, formt, unit) in sorted_data:
            slice_ = self.series.append(app, formt)
            slice_.setProperty("display_value", display_value)
            slice_.setProperty("unit", unit)

            slice_.hovered.connect(self.on_slice_hovered)

        if other:
            total_formt = sum(v[1] for _, v in other)

            slice_other = self.series.append("Другое", total_formt)

            total_sec, unit = get_display_value_and_unit(total_formt * 60)

            slice_other.setProperty("display_value", total_sec)
            slice_other.setProperty("unit", unit)

            slice_other.hovered.connect(self.on_slice_hovered)

        self.category_stats_series.clear()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        if not data_dict:
            self.category_axis_y.setRange(0, 60)
            self.category_stats_axis_x.setCategories([])
            return

        categories = [""]
        max_minutes = 0

        self.category_stats_axis_x.setCategories([""])

        for cat, (disp_val, minutes, unit) in data_dict.items():
            if minutes <= 0:
                continue

            barset = QBarSet(cat)
            barset.append(minutes // 60)
            self.category_stats_series.append(barset)

            max_minutes = max(max_minutes, minutes)

            barset.hovered.connect(
                lambda status, index, bs=barset, v=disp_val, u=unit:
                self.show_tooltip(status, bs, v, u) if status else None
            )

        if max_minutes > 0:
            self.category_axis_y.setRange(0, 1440)
        else:
            self.category_axis_y.setRange(0, 1)

        # self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.category_stats_chart.update()