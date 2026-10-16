from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt
from modules.core import approximate_byte_size


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

        else:
            return approximate_byte_size(
                self.text(1)) < approximate_byte_size(other.text(1))
