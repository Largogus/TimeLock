from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget
from core.system.date import normal_time, to_time, plural


class CircleProgressBar(QWidget):
    def __init__(self, limit):
        super().__init__()
        self.progress = 0
        self.limit = limit
        self.setMinimumSize(50, 50)
        self.setMaximumSize(250, 250)

        self.time = ""
        print(limit)

    def upd(self, post_progress):
        if self.progress == post_progress:
            return
        self.progress = post_progress
        self.time = normal_time(self.progress)
        self.update()

    def setLimit(self, new_limit):
        self.limit = new_limit
        print(self.limit)
        self.update()

    def progressColor(self) -> QColor:
        if self.limit == 0:
            return QColor("#71d926")

        percent = (self.progress / self.limit)

        if percent <= 25:
            return QColor("#4CAF50")
        elif 25 > percent <= 50:
            return QColor("#1c731f")
        elif 50 > percent <= 75:
            return QColor("#FFEB3B")
        elif 75 > percent <= 100:
            return QColor("#F44336")
        else:
            return QColor("#F44336")

    def paintEvent(self, event):
        if self.height() > self.width():
            self.setFixedWidth(self.height())
        if self.width() > self.height():
            self.setFixedHeight(self.width())

        if self.limit != 0:
            progress_degree = (self.progress / self.limit) * 360
        else:
            progress_degree = (self.progress / 86400) * 360

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = self.width() / 10
        pen_width = self.width() // 25

        rect = QRectF(
            margin / 2,
            margin / 2,
            self.width() - margin,
            self.height() - margin
        )

        bg_pen = QPen(Qt.GlobalColor.gray)
        bg_pen.setWidth(pen_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(bg_pen)
        painter.drawArc(rect, 0, 460 * 16)

        progress_pen = QPen(self.progressColor())
        progress_pen.setWidth(pen_width)
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(progress_pen)
        painter.drawArc(rect, 90 * 16, -progress_degree * 16)

        font = QFont()
        font.setPointSize(int(self.height() / 16))

        painter.setFont(font)

        text = self.time

        if self.limit == 0:
            painter.setPen(QColor('#2b2b2b'))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)
        else:
            text_rect_s = QRectF(rect)
            text_rect_s.setTop(rect.top() + 20)

            text_rect_l = QRectF(rect)
            text_rect_l.setTop(rect.top() - 15)

            painter.setPen(QColor('#2b2b2b'))

            painter.drawText(text_rect_l, Qt.AlignmentFlag.AlignCenter, text)

            font.setPointSize(int(self.height() / 24))
            painter.setFont(font)

            if self.limit < 60 * 60:
                h = to_time(self.limit, "m")
                t_h = plural(h, ("минута", "минуты", "минут"))
            else:
                h = to_time(self.limit)
                t_h = plural(h, ("час", "часа", "часов"))

            painter.setPen(QColor('#555555'))

            painter.drawText(text_rect_s, Qt.AlignmentFlag.AlignCenter, f"из {h} {t_h}")

    def sizeHint(self) -> QSize:
        return QSize(260, 260)