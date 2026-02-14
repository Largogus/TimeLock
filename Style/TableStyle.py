from PySide6.QtCore import QRect, Signal, QModelIndex
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle, QApplication


class TableDelegate(QStyledItemDelegate):
    click_btn = Signal(QModelIndex)

    def paint(self, painter, option, index):
        if index.column() == 5:
            button_option = QStyleOptionButton()
            button_option.rect = QRect(
                option.rect.center().x() - 14,
                option.rect.center().y() - 14,
                28,
                28
            )
            button_option.text = "…"
            button_option.state = QStyle.StateFlag.State_Enabled

            button_option.palette = option.palette

            QApplication.style().drawControl(
                QStyle.ControlElement.CE_PushButtonLabel,
                button_option,
                painter
            )
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.column() == 5 and event.Type.MouseButtonRelease:

            button_rect = QRect(
                option.rect.center().x() - 14,
                option.rect.center().y() - 14,
                28,
                28
            )

            if button_rect.contains(event.pos()):
                self.click_btn.emit(index)
                return True

        return super().editorEvent(event, model, option, index)