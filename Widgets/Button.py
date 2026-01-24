from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QPixmap, QFont


class Button(QPushButton):
    def __init__(self, name: str,
                 font_size: int = 14,
                 radius: int = 15,
                 min: int = 165,
                 max: int = 500,
                 alpha: list[int, int, int] = None,
                 image_path: str = None,
                 ratio: int = 2,
                 scale: int = 0,
                 icon_size: int = 24,
                 margin: int = 12,
                 indicator: bool = False):
        super().__init__()

        self.RADIUS = radius
        self.BG_COLOR = QColor('#B6B6B6')
        self.PRESSER_COLOR = QColor('#969696')
        self.HOVERED_COLOR = QColor('#ADADAD')
        self.INDICATOR_COLOR = QColor("#5bff3b")
        self.ALPHA = alpha if alpha is not None else [255, 255, 255]
        self.RATIO = ratio
        self.SCALE = scale
        self.MARGIN = margin

        self.ICON_SIZE = icon_size

        self.INDICATOR = indicator

        self.alpha_color, self.alpha_hover, self.alpha_pressed = [i for i in self.ALPHA]

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.BORDER_WIDTH = 1

        self.setMinimumHeight(40)
        self.setMinimumWidth(min)

        self.setMaximumWidth(max)

        self.name = name
        self.hovered = False
        self.FONT_SIZE = font_size

        self.setMouseTracking(True)

        self.pixmap = QPixmap(image_path) if image_path else None

        if self.INDICATOR:
            self.indicator_anim = QPropertyAnimation(self, b"indicatorColor")
            self.indicator_anim.setDuration(400)
            self.INDICATOR_OFFSET = self.RADIUS * 2 + self.MARGIN

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        draw_rect = QRectF(rect)

        if self.isDown():
            color = self.PRESSER_COLOR
            color.setAlpha(self.alpha_pressed)
        elif self.hovered:
            color = self.HOVERED_COLOR
            color.setAlpha(self.alpha_hover)
        else:
            color = self.BG_COLOR
            color.setAlpha(self.alpha_color)

        paint.setBrush((QBrush(color)))
        paint.setPen(Qt.PenStyle.NoPen)

        paint.drawRoundedRect(draw_rect, self.RADIUS, self.RADIUS)

        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(
                self.ICON_SIZE,
                self.ICON_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (rect.width() - scaled_pixmap.width()) // self.RATIO
            y = (rect.height() - scaled_pixmap.height()) // 2
            paint.drawPixmap(x + (self.SCALE * 2), y, scaled_pixmap)

        if self.pixmap:
            text_rect = QRectF(draw_rect)
            text_rect.setLeft(rect.left() + (10 * 4))
        else:
            text_rect = QRectF(draw_rect)

        if self.INDICATOR:
            text_rect.setLeft(rect.left() + (10 * 4))
            paint.setBrush(self.INDICATOR_COLOR)
            paint.setPen(Qt.PenStyle.NoPen)
            paint.drawEllipse(self.INDICATOR_OFFSET, self.INDICATOR_OFFSET - 1, self.RADIUS * 2, self.RADIUS * 2)

        painter_font = paint.font()
        painter_font.setPixelSize(self.FONT_SIZE)
        painter_font.setWeight(QFont.Weight.Bold)
        paint.setFont(painter_font)
        paint.setPen(Qt.GlobalColor.black)

        paint.setClipRect(text_rect)
        paint.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.name)

    def setPixmap(self, path: str):
        self.pixmap = QPixmap(path)
        self.update()

    def setBackgroundColor(self, color: QColor = QColor('#B6B6B6')):
        self.BG_COLOR = color
        self.update()

    def setBackgroundHover(self, color: QColor = QColor('#ADADAD')):
        self.HOVERED_COLOR = color
        self.update()

    def setBackgroundPressed(self, color: QColor = QColor('#969696')):
        self.PRESSER_COLOR = color
        self.update()

    def getIndicatorColor(self):
        return self.INDICATOR_COLOR

    def setIndicatorColor(self, color: QColor):
        self.INDICATOR_COLOR = color
        self.update()

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.INDICATOR:
            self.indicator_anim.stop()
            self.indicator_anim.setStartValue(self.INDICATOR_COLOR)

            if self.getIndicatorColor() == QColor("#5bff3b"):
                self.indicator_anim.setEndValue(QColor("#c41000"))
            else:
                self.indicator_anim.setEndValue(QColor("#5bff3b"))

            self.indicator_anim.start()

        super().mousePressEvent(event)

    indicatorColor = Property(QColor, lambda self: self.INDICATOR_COLOR, lambda self, c: self.setIndicatorColor(c))
