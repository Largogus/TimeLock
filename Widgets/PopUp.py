from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QStyledItemDelegate, QStyle
from PySide6.QtGui import QColor, Qt, QPainter, QBrush, QPen, QFont
from PySide6.QtCore import QSize, Signal


class SlotPopUp(QListWidget):

    itemClicked = Signal(str)

    def __init__(self,
                 item: set = None,
                 background: QColor = QColor(255, 255, 255),
                 border: int = 6,
                 font_size: int = 16,
                 background_hover: QColor = QColor('#ADADAD')):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        self.BACKGROUND = background
        self.BACKGROUND_HOVER = background_hover
        self.BORDER_RADIUS = border
        self.FONT_SIZE = font_size
        self.list = item or []
        self.hovered = False

        self.setItemDelegate(MyDelegate(self))

        self._getItem(item or [])

        self.clicked.connect(self.on_item_clicked)

    def on_item_clicked(self, index):
        select = self.model().data(index)
        self.itemClicked.emit(select)

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.hovered:
            color = self.BACKGROUND_HOVER
        else:
            color = self.BACKGROUND

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRect(self.rect())

        super().paintEvent(event)

    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)

    def mousePressEvent(self, event):
        self.hide()
        super().mousePressEvent(event)

    def _getItem(self, new_items: set):
        self.clear()
        self.list = new_items

        for i in self.list:
            item = QListWidgetItem(i)

            self.addItem(item)

        self.setMaximumHeight(37 * len(self.list))


class PopUp(QWidget):

    TextToTextEdit = Signal(str)

    def __init__(self,
                 item: list = None,
                 text: str = "",
                 background: QColor = QColor(255, 255, 255),
                 border_radius: int = 6,
                 font_size: int = 16,
                 slot_bg: QColor = QColor('#C8C8C8'),
                 background_hover: QColor = QColor('#ADADAD')):
        super().__init__()

        self.setMinimumSize(300, 40)

        self.setMouseTracking(True)

        self.TEXT = text
        self.BACKGROUND = background
        self.BACKGROUND_HOVERED = background_hover
        self.BORDER_RADIUS = border_radius
        self.FONT_SIZE = font_size
        self.slot_bg = slot_bg
        self._error = False

        self.hovered = False

        self.main = QVBoxLayout()
        self.popup = SlotPopUp(item=item, background=self.slot_bg, font_size=self.FONT_SIZE)

        self.popup.itemClicked.connect(self.on_popup_item_clicked)

        self.setLayout(self.main)

    def addItemList(self, item):
        self.popup._getItem(item)

    def on_popup_item_clicked(self, item):
        self.TEXT = f'{item} ▼'
        self.TextToTextEdit.emit(item)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        if self.hovered:
            color = self.BACKGROUND_HOVERED
        else:
            color = self.BACKGROUND

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)

        font = painter.font()
        font.setPixelSize(self.FONT_SIZE)
        painter.setFont(font)

        if self._error:
            rect.adjust(2, 2, -2, -2)
            painter.setPen(QPen(QColor("red"), 2))
            painter.drawRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.TEXT)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if not self.popup.isVisible():
            self.popup.setFixedWidth(self.width())

            global_pos = self.mapToGlobal(self.rect().bottomLeft()) #!!!
            self.popup.move(global_pos)

            self.popup.setFocus()
            self.popup.show()
        else:
            self.popup.hide()

        self.update()

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def setError(self, value: bool):
        self._error = value

        self.update()


class MyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor(140, 140, 140, 100))
        else:
            pass

        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, QColor("#ADADAD"))
        else:
            pass

        painter.setFont(QFont("Arial", 14))
        painter.setPen(QColor("black"))
        text = index.data()
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(0, 35)