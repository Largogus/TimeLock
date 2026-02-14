from PySide6.QtCore import QSortFilterProxyModel
from core.system.date import parse_time


class SortFilter(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.category_filter = ""
        self.name_filter = ""
        self.limit_filter = ""
        self.time_filter = None

    def filterAcceptsRow(self, source_row, source_parent):
        index_category = self.sourceModel().index(source_row, 1, source_parent)
        category_data = self.sourceModel().data(index_category)

        index_name = self.sourceModel().index(source_row, 0, source_parent)
        name_data = self.sourceModel().data(index_name)

        index_limit = (self.sourceModel().index(source_row, 3))
        limit_data = self.sourceModel().data(index_limit)

        index_time = (self.sourceModel().index(source_row, 2))
        time_data = self.sourceModel().data(index_time)

        category_data = (category_data or "")
        name_data = (name_data or "").lower()
        limit_data = str(limit_data or "")
        time_data = str(time_data or "")

        category_ok = (self.category_filter == "" or self.category_filter == category_data)
        name_ok = (self.name_filter == "" or self.name_filter.lower() in name_data)
        limit_ok = True

        if self.limit_filter == "" or self.limit_filter is None: limit_ok = True
        elif self.limit_filter == "Без лимита" or self.limit_filter == "Нет": limit_ok = limit_data == "Нет"
        elif self.limit_filter == "С лимитом": limit_ok = limit_data != "Нет"

        time_ok = (self.time_filter is None or self.time_filter in time_data)

        return category_ok and name_ok and limit_ok and time_ok

    def updateName(self, name):
        self.name_filter = name
        self.invalidateFilter()

    def updateCategory(self, category):
        self.category_filter = category
        self.invalidateFilter()

    def updateLimit(self, limit):
        self.limit_filter = limit
        self.invalidateFilter()

    # def updateTime(self, name):
    #     self.name_filter = name
    #     self.invalidateFilter()

    def lessThan(self, source_left, source_right):
        col = source_left.column()
        left_data = self.sourceModel().data(source_left)
        right_data = self.sourceModel().data(source_right)

        if col == 0:
            return str(left_data).lower() < str(right_data).lower()
        elif col == 2:
            return parse_time(left_data) < parse_time(right_data)
        elif col == 3:
            return parse_time(left_data) < parse_time(right_data)
        else:
            return str(left_data) < str(right_data)
