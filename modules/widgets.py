from PyQt6.QtWidgets import QTreeWidgetItem, QTableWidgetItem
from PyQt6.QtCore import Qt
from modules.core import (
    approximate_byte_size
)


class TorrentFileTreeItem(QTreeWidgetItem):
    def __init__(self, texts, is_folder: bool = False):
        super().__init__(texts)
        self._is_folder = is_folder

    def __lt__(self, other):
        tree = self.treeWidget()
        if tree is None:
            return super().__lt__(other)

        column = tree.sortColumn()
        order = tree.header().sortIndicatorOrder()
        ascending = (order == Qt.SortOrder.AscendingOrder)

        other_is_folder = getattr(other, "_is_folder", False)

        if self._is_folder != other_is_folder:
            if ascending:
                return self._is_folder
            else:
                return not self._is_folder

        if column == 0:
            return self.text(0).lower() < other.text(0).lower()

        elif column == 1:
            return self.text < getattr(other, "_sort_size", 0)

        elif column == 2:
            return getattr(self, "_progress", 0) < getattr(other, "_progress", 0)

        return super().__lt__(other)


class TorrentFileItem(QTableWidgetItem):
    def __init__(self, text: str, sort_value):
        super().__init__(text)
        if hasattr(sort_value, "value"):
            self._sort_value = sort_value.value
        else:
            self._sort_value = sort_value

    def __lt__(self, other):
        table = self.tableWidget()
        if table is None:
            return super().__lt__(other)

        that = self._sort_value
        other = other._sort_value

        column = table.horizontalHeader().sortIndicatorSection()

        if column in (1, 2, 4, 5, 6, 7):
            try:
                return float(that) < float(other)
            except Exception:
                return True

        try:
            return that.text().lower() < other.text().lower()
        except Exception:
            try:
                return that.lower() < other.lower()
            except Exception:
                return str(that).lower() < str(other).lower()
