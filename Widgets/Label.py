from PySide6.QtGui import QColor, Qt, QPainter, QFont
from PySide6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(self, text: str,
                 background_color: QColor | Qt.GlobalColor = Qt.GlobalColor.black,
                 alpha: int = 255,
                 color_text: QColor | Qt.GlobalColor = Qt.GlobalColor.black,
                 color_size: int = 15,
                 bold: bool = False,
                 align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
        super().__init__()

        self.text = text
        self._bg = background_color
        self._alpha = alpha
        self._color_text = color_text
        self._color_size = color_size
        self._align = align
        self._bold = bold

    def setTextPlace(self, text):
        self.setText(text)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(self._bg)
        bg.setAlpha(self._alpha)

        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRect(self.rect())

        painter_font = painter.font()

        if self._bold:
            painter_font.setWeight(QFont.Weight.Bold)

        painter_font.setPixelSize(self._color_size)
        painter.setFont(painter_font)
        painter.setPen(self._color_text)

        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignVCenter | self._align, self.text)

        super().paintEvent(event)