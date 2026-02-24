from PySide6.QtGui import QColor, QPainter, QPen, Qt
from PySide6.QtWidgets import QStyle, QStyledItemDelegate


class PopupStyle(QStyledItemDelegate):
    def __init__(self, bg, hbg, clc_bg, text_color):
        super().__init__()
        self._bg = bg
        self._hbg = hbg
        self._clc_bg = clc_bg
        self._text_color = text_color

    def paint(self, painter: QPainter, option, index):
        painter.save()

        rect = option.rect

        if option.state & QStyle.StateFlag.State_Selected:
            color = QColor(self._clc_bg)
            color.setAlpha(255)
            painter.fillRect(option.rect, color)
        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, self._hbg)
        else:
            painter.fillRect(option.rect, self._bg)

        text = index.data(Qt.ItemDataRole.DisplayRole)

        painter.setPen(QPen(self._text_color))
        painter.setFont(option.font)

        text_rect = rect.adjusted(8, 0, -8, 0)

        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            text
        )

        painter.restore()