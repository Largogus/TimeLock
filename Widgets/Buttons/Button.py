from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QBrush, QColor, QFont
from Widgets.Modal.DisabledMessageModal import show_disabled_message


class Button(QPushButton):
    def __init__(self, name: str,
                 font_size: int = 14,
                 font_color: Qt.GlobalColor | QColor = Qt.GlobalColor.black,
                 radius: int = 15,
                 min: int = 165,
                 maxs: int = 500,
                 alpha: list[int, int, int] = None,
                 svg_path: str = None,
                 ratio: int = 2,
                 scale: int = 0,
                 icon_size: int = 24,
                 margin: int = 6,
                 align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
                 argument: str | int = None,
                 disabled_text: str = ""):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.Fixed)

        self.RADIUS = radius
        self.BG_COLOR = QColor('#B6B6B6')
        self.PRESSER_COLOR = QColor('#969696')
        self.HOVERED_COLOR = QColor('#ADADAD')
        self.ALPHA = alpha if alpha is not None else [255, 255, 255]
        self.RATIO = ratio
        self.SCALE = scale
        self.MARGIN = margin
        self.ALIGN = align
        self.DISABLED_TEXT = disabled_text
        self.DISABLED = False

        self.ICON_SIZE = icon_size

        self.alpha_color, self.alpha_hover, self.alpha_pressed = [i for i in self.ALPHA]

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.BORDER_WIDTH = 1

        self.setMinimumHeight(40)
        self.setMinimumWidth(min)

        self.setMaximumWidth(maxs)

        self.name = name
        self.hovered = False
        self.FONT_SIZE = font_size
        self.FONT_COLOR = font_color

        self.ARG = argument

        self.setMouseTracking(True)

        self.renderer = QSvgRenderer(svg_path) if svg_path else None

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

        if self.DISABLED:
            color = self.BG_COLOR
            color.setAlpha(self.alpha_color)

        paint.setBrush((QBrush(color)))
        paint.setPen(Qt.PenStyle.NoPen)

        paint.drawRoundedRect(draw_rect, self.RADIUS, self.RADIUS)

        if not self.DISABLED:
            pass
        else:
            black_color = QColor('black')
            black_color.setAlpha(100)

            paint.setBrush((QBrush(black_color)))
            paint.setPen(Qt.PenStyle.NoPen)

            paint.drawRoundedRect(draw_rect, self.RADIUS, self.RADIUS)

        if self.renderer:
            icon_rect = QRectF(
                self.MARGIN,
                (rect.height() - self.ICON_SIZE) / 2,
                self.ICON_SIZE,
                self.ICON_SIZE
            )
            self.renderer.render(paint, icon_rect)

        if self.renderer:
            text_rect = QRectF(draw_rect)
            text_rect.setLeft(rect.left() + (10 * 4))
        else:
            text_rect = QRectF(draw_rect)

        painter_font = paint.font()
        painter_font.setPixelSize(self.FONT_SIZE)
        painter_font.setWeight(QFont.Weight.Bold)
        paint.setFont(painter_font)
        paint.setPen(self.FONT_COLOR)

        paint.setClipRect(text_rect)

        paint.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | self.ALIGN, self.name)

    def setImage(self, path: str):
        self.renderer = QSvgRenderer(path)
        self.update()

    def setDisabledText(self, text):
        self.DISABLED_TEXT = text

    def setBackgroundColor(self, color: QColor = QColor('#B6B6B6')):
        self.BG_COLOR = color
        self.update()

    def setBackgroundHover(self, color: QColor = QColor('#ADADAD')):
        self.HOVERED_COLOR = color
        self.update()

    def setBackgroundPressed(self, color: QColor = QColor('#969696')):
        self.PRESSER_COLOR = color
        self.update()

    def setText(self, text):
        self.name = text
        self.update()

    def setDisabled(self, arg__1):
        self.DISABLED = arg__1
        self.update()

    def getText(self) -> str:
        return self.name

    def getArg(self) -> str | int:
        return self.ARG

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.DISABLED:
            show_disabled_message(text=self.DISABLED_TEXT)

            return

        super().mousePressEvent(event)