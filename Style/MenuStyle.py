from PySide6.QtGui import QPalette, QColor, QPainter, Qt, QPen
from PySide6.QtWidgets import QProxyStyle, QStyle


class MenuStyle(QProxyStyle):
    def drawControl(self, element, option, painter, widget =None):
        if element == QStyle.ControlElement.CE_MenuItem:
            painter.save()

            rect = option.rect

            if option.state & QStyle.StateFlag.State_Selected:
                painter.setBrush(QColor(135, 255, 137, 100))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRect(rect.adjusted(4, 2, -4, -2))

            painter.setPen(QPen(QColor("#0000000")))

            text_rect = rect.adjusted(12, 0, -12, 0)
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                option.text
            )

            painter.restore()
            return

        super().drawControl(element, option, painter, widget)

    def drawPrimitive(self, element, option, painter, widget =None):
        if element == QStyle.PrimitiveElement.PE_PanelMenu:
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            rect = option.rect

            painter.setBrush(QColor('white'))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)

            painter.restore()
            return

        super().drawPrimitive(element, option, painter, widget)