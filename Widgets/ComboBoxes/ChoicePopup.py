from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QComboBox, QListView, QStyledItemDelegate, QStyle
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect, QRectF, Signal


class FancyDelegate(QStyledItemDelegate):
    def __init__(self, bg: QColor | Qt.GlobalColor, hbg: QColor | Qt.GlobalColor,
                 clickbg: QColor | Qt.GlobalColor, text_bg: QColor | Qt.GlobalColor = Qt.GlobalColor.white,
                 font_size: int = 25):
        super().__init__()
        self._bg = bg
        self._hbg = hbg
        self._clc_bg = clickbg
        self._text_bg = text_bg
        self._font_size = font_size

    def paint(self, painter: QPainter, option, index):
        painter.save()

        rect = option.rect.adjusted(8, 0, -8, 0)

        if option.state & QStyle.StateFlag.State_Selected:
            color = QColor(self._hbg)
            color.setAlpha(255)
            painter.fillRect(option.rect, color)
        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, self._clc_bg)
        else:
            painter.fillRect(option.rect, self._bg)

        font = painter.font()
        font.setPixelSize(self._font_size)
        font.setBold(True)
        painter.setFont(font)

        text = index.data(Qt.ItemDataRole.DisplayRole)
        painter.setPen(QPen(self._text_bg))
        painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option, index):
        hint = super().sizeHint(option, index)
        hint.setHeight(self._font_size + 12)
        return hint


class ChoicePopup(QComboBox):
    close = Signal()

    def __init__(self,
                 bg: QColor | Qt.GlobalColor = QColor('#f5f5f8'),
                 bg_hover: QColor | Qt.GlobalColor = QColor('#e3e3e6'),
                 bg_hover_box: QColor | Qt.GlobalColor = QColor(227, 227, 230, 120),
                 bg_focus: QColor | Qt.GlobalColor = QColor(201, 201, 201, 150),
                 bg_text_color: QColor | Qt.GlobalColor = Qt.GlobalColor.black,
                 bg_text_color_box: QColor | Qt.GlobalColor = Qt.GlobalColor.black,
                 font_size: int = 20,
                 fixed_width: int = 250):
        super().__init__()

        self.setFixedWidth(fixed_width)
        self.setFixedHeight(font_size * 2)

        self._bg_color = bg
        self._bg_hover = bg_hover
        self._bg_hover_box = bg_hover_box
        self._bg_focus = bg_focus
        self._bg_text_color = bg_text_color
        self._bg_text_color_box = bg_text_color_box
        self._font_size = font_size

        self.setView(QListView())
        self.setItemDelegate(FancyDelegate(self._bg_color, self._bg_hover_box, self._bg_focus, self._bg_text_color_box, self._font_size))

        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._border_color = QColor("#ADADAD")
        self._radius = 6
        self._has_selection = False
        self._select = None

        self._hover = False
        self._focused = False
        self._clear_rect = None

        self.currentIndexChanged.connect(self._on_click)

        self.renderer = QSvgRenderer('src/icon/drop_down.svg')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        if self._focused:
            bg = self._bg_focus
        elif self._hover:
            bg = self._bg_hover
        else:
            bg = self._bg_color

        painter.setBrush(bg)
        painter.setPen(QPen(self._border_color))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), self._radius, self._radius)

        font = painter.font()
        font.setPixelSize(self._font_size)
        font.setBold(True)
        painter.setFont(font)

        if self._has_selection:
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(self._select or "")

            size = 12
            margin = 8
            x = rect.left() + 8 + text_width + margin
            y = (rect.center().y() - size // 2) + (self._font_size // 5)
            self._clear_rect = QRect(x, y, size, size)

            painter.setPen(QPen(self._bg_text_color, 2))

            painter.drawText(rect.adjusted(8, 0, -25, 0),
                             Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                             self._select)

        arrow_size = 32
        arrow_margin = 32

        rect_svg = QRectF(
            (rect.right() - arrow_margin),
            (rect.height() - arrow_size) / 2,
            arrow_size,
            arrow_size)

        self.renderer.render(painter, rect_svg)

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def showPopup(self):
        self._focused = True
        self.update()
        super().showPopup()

    def hidePopup(self):
        self._focused = False
        self.update()
        super().hidePopup()

    def _on_click(self):
        self._has_selection = True
        self._select = self.currentText()
        self.update()