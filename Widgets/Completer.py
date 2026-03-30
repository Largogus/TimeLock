from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import QLineEdit, QCompleter


class Completer(QCompleter):
    def __init__(self, line_edit: QLineEdit, items: list[str]):
        super().__init__(items, line_edit)
        self.line_edit = line_edit
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        line_edit.setCompleter(self)

    def update_items(self, new_items: list[str]):
        model = QStringListModel(new_items)
        self.setModel(model)
