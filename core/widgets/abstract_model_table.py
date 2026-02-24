from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.apps_data = []

    def update_data(self, apps_data):
        new_apps_dict = {app["id"]: app for app in apps_data}

        for row, app in enumerate(self.apps_data):
            new_app = new_apps_dict.get(app["id"])
            if not new_app:
                continue

            changed_columns = []

            if app["today_time"] != new_app["today_time"]:
                app["today_time"] = new_app["today_time"]
                changed_columns.append(2)

            if app["status"] != new_app["status"]:
                app["status"] = new_app["status"]
                changed_columns.append(4)

            for col in changed_columns:
                index = self.index(row, col)
                self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])

        existing_ids = {app["id"] for app in self.apps_data}
        for new_app in apps_data:
            if new_app["id"] not in existing_ids:
                row = len(self.apps_data)
                self.beginInsertRows(QModelIndex(), row, row)
                self.apps_data.append(new_app)
                self.endInsertRows()

    def rowCount(self, parent=None):
        return len(self.apps_data)

    def columnCount(self, parent=None):
        return 6

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        app = self.apps_data[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return app["name"]
            if col == 1:
                return app["category"] if app["category"] is not None else "Без категории"
            if col == 2:
                return app["today_time"]
            if col == 3:
                return app["limit"] if app['limit'] != 0 else "Нет"
            if col == 4:
                return "🟢" if app["status"] else "🔴"
            if col == 5:
                return "..."

        if role == Qt.ItemDataRole.UserRole:
            if col == 5:
                return app['name']
            else:
                return app["id"]

        if role == Qt.ItemDataRole.TextAlignmentRole and col != 0:
            return Qt.AlignmentFlag.AlignCenter

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ["Название", "Категория", "Сегодня", "Лимит", "Статус", ''][section]

    def updateCategoryInTable(self, app_name: str, new_category: str):

        row_to_update = next(
            (i for i, app in enumerate(self.apps_data) if app["name"] == app_name),
            None
        )
        if row_to_update is not None:
            self.apps_data[row_to_update]["category"] = new_category

            index = self.index(row_to_update, 1)

            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])