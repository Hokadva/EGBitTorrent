from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QToolBar, QLineEdit, QComboBox, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar,
    QListWidget, QListWidgetItem, QTabWidget, QStatusBar,
    QHeaderView, QAbstractItemView, QFileDialog, QMessageBox, QDialog,
    QDialogButtonBox, QGroupBox, QCheckBox, QGridLayout, QTreeWidget,
    QTextEdit, QSizePolicy
)
from modules.torrent import TorrentFile
from PyQt6.QtGui import QAction, QColor
from modules.widgets import TorrentFileTreeItem, TorrentFileItem
import os
import datetime
import qtawesome as qta
from modules.torrent import TorrentState, DuplicateTorrentError
from modules.themes import THEMES
from modules.validator import (
    validate_save_path, validate_magnet, validate_torrent_file
)
import libtorrent as lt
from modules.core import (
    human_size, get_free_disk_space, find_common_root,
    new_root_if_necessary, smart_folder_creating, extract_magnet_name,
    human_rate, colorize, Colors, folder_remove
)


class RemoveTorrent(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        self.setMinimumSize(200, 100)
        self.setWindowTitle("Remove torrent")
        remove_torrent_layout = QVBoxLayout()
        self.setLayout(remove_torrent_layout)

        confirm_label = QLabel(
            "Do you really want to delete these torrents")
        self._delete_file_checkbox = QCheckBox("Also delete the uploaded files?")
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok
                            ).setText("Accept")
        buttons.button(QDialogButtonBox.StandardButton.Cancel
                            ).setText("Cancel")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        remove_torrent_layout.addWidget(confirm_label)
        remove_torrent_layout.addWidget(self._delete_file_checkbox)
        remove_torrent_layout.addWidget(buttons)

    @property
    def is_remove_files(self) -> bool:
        return self._delete_file_checkbox.isChecked()


class AddMagnetWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        self.setMinimumWidth(300)
        self.setWindowTitle("Add torrent by magnet link")
        magnet_main_layout = QVBoxLayout()
        self.setLayout(magnet_main_layout)

        self._link_field = QTextEdit()
        self._link_field.clear()
        self._link_field.setPlaceholderText("magnet:?xt=urn:btih:...")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok
                            ).setText("Accept")
        buttons.button(QDialogButtonBox.StandardButton.Cancel
                            ).setText("Cancel")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        magnet_main_layout.addWidget(self._link_field)
        magnet_main_layout.addWidget(buttons)

    @property
    def magnet_link(self):
        return self._link_field.toPlainText().strip()


class AddTorrentWindow(QDialog):
    def __init__(
            self, default_save_path: str, parent, torrent: str,
            is_magnet: bool = False):
        super().__init__(parent)

        self.torrent = torrent

        self.setWindowTitle("Add torrent")
        self.resize(820, 560)

        self._default_save_path = default_save_path

        if not is_magnet:
            self._load_torrent_info()
            self.build_ui()
            self._apply_torrent_info(self._torrent_info)
            self._update_free_space()

        else:
            self._torrent_info = None
            self.build_ui()
            self._display_free_space()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(12)

        top.addLayout(self._build_left_panel(), 1)
        top.addLayout(self._build_right_panel(), 1)

        root.addLayout(top, 1)

        root.addWidget(self._build_bottom_panel())

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Add")
        self.buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        root.addWidget(self.buttons)

        self._button_box = self.buttons

    def _build_left_panel(self):
        panel = QVBoxLayout()
        panel.setSpacing(10)

        save_group = QGroupBox("Save folder")
        svg = QVBoxLayout(save_group)

        row = QHBoxLayout()
        row.setSpacing(6)

        self.path_edit = QLineEdit(self._default_save_path)
        self.path_edit.textChanged.connect(self._update_free_space)
        self.path_edit.textEdited.connect(self._update_free_space)
        row.addWidget(self.path_edit, 1)

        browse_dir_btn = QPushButton(
            qta.icon("fa5s.folder-open", color="#9aa1ac"), ""
        )
        browse_dir_btn.setFixedWidth(34)
        browse_dir_btn.clicked.connect(self._on_browse_dir)
        row.addWidget(browse_dir_btn)

        svg.addLayout(row)

        self.free_space_label = QLabel("Free disc-space: -")
        self.free_space_label.setStyleSheet(
            "color: #9aa1ac; font-size: 11px;")
        svg.addWidget(self.free_space_label)

        panel.addWidget(save_group)

        groups_group = QGroupBox("Groups")
        gg = QVBoxLayout(groups_group)
        gg.setSpacing(4)

        self.group_checkboxes = {}

        panel.addWidget(groups_group)

        self.start_now_cb = QCheckBox("Start downloading right now")
        self.start_now_cb.setChecked(True)
        panel.addWidget(self.start_now_cb)

        self.create_folder_cb = QCheckBox("Create folder for torrent")
        self.create_folder_cb.setChecked(True)
        panel.addWidget(self.create_folder_cb)

        panel.addStretch(1)

        return panel

    def _build_right_panel(self):
        panel = QVBoxLayout()
        panel.setSpacing(10)

        files_group = QGroupBox("Files:")
        fg = QVBoxLayout(files_group)

        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabels(["Name", "Size"])
        self.files_tree.setColumnCount(2)
        self.files_tree.setAlternatingRowColors(True)
        self.files_tree.setRootIsDecorated(True)
        self.files_tree.setUniformRowHeights(True)
        self.files_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.files_tree.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        header = self.files_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        fg.addWidget(self.files_tree)

        self.files_status = QLabel("-")
        self.files_status.setStyleSheet("color: #9aa1ac; font-size: 11px;")
        fg.addWidget(self.files_status)

        panel.addWidget(files_group, 1)

        return panel

    def _build_bottom_panel(self):
        box = QGroupBox("Torrent information")
        grid = QGridLayout(box)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(6)
        grid.setContentsMargins(12, 12, 12, 12)

        def add_row(r, label, value_widget):
            lbl = QLabel(f"{label}:")
            lbl.setStyleSheet("color: #9aa1ac;")
            grid.addWidget(lbl, r, 0, Qt.AlignmentFlag.AlignRight)
            grid.addWidget(value_widget, r, 1, 1, 3)

        self.info_name = QLabel("-")
        add_row(0, "Name", self.info_name)

        self.info_size = QLabel("-")
        self.info_date = QLabel("-")
        row1 = QHBoxLayout()
        row1.setSpacing(24)
        row1.addWidget(QLabel("Size:"))
        row1.addWidget(self.info_size)
        row1.addSpacing(20)
        row1.addWidget(QLabel("Date of creation:"))
        row1.addWidget(self.info_date)
        row1.addStretch(1)
        grid.addLayout(row1, 1, 1, 1, 3)

        self.info_comment = QLabel("-")
        self.info_comment.setWordWrap(True)
        add_row(2, "Comment:", self.info_comment)

        return box

    def _on_browse_dir(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Choose save folder:",
            self.path_edit.text() or self._default_save_path,
        )
        if path:
            self.path_edit.setText(path)

    def _display_free_space(self) -> int:
        path = self.path_edit.text().strip()

        if not path:
            self.free_space_label.setText("Free disc space: -")
            return

        if not os.path.exists(path) or not os.path.isdir(path):
            self.free_space_label.setText(
                colorize(f"Path doesn't exists: {path}", Colors.error_red)
            )
            self._change_apply_btn_status(False)
            return

        free = get_free_disk_space(path)
        if free > 0:
            self.free_space_label.setText(
                f"Free disc space: {human_size(free)}"
            )
        else:
            self.free_space_label.setText("Free disc space: -")
            self._change_apply_btn_status(False)

        self._change_apply_btn_status(True)
        return free

    def _update_free_space(self):
        free = self._display_free_space()

        if free is None or self._torrent_info is None:
            return

        if free < self._torrent_info.total_size():
            self._change_apply_btn_status(False)
            return

        self._change_apply_btn_status(True)

    def _change_apply_btn_status(self, status):
        accept_btn = self.buttons.button(QDialogButtonBox.StandardButton.Ok)
        if status:
            accept_btn.setEnabled(True)
            return

        accept_btn.setEnabled(False)

    def _load_torrent_info(self):
        """Загружает метаданные из .torrent-файла и обновляет UI."""
        try:
            info = lt.torrent_info(self.torrent)

        except Exception as e:
            self._torrent_info = None
            self.files_table.setRowCount(0)
            self.files_status.setText(f"Read error: {e}")
            self.info_name.setText("-")
            self.info_size.setText("-")
            self.info_date.setText("-")
            self.info_comment.setText("-")
            return

        self._torrent_info = info

    def _apply_torrent_info(self, info):
        """Заполняет UI данными из lt.torrent_info."""
        self.info_name.setText(info.name() or "-")
        self.info_size.setText(human_size(info.total_size()))

        created = info.creation_date()
        if created and created > 0:
            self.info_date.setText(
                datetime.datetime.fromtimestamp(created
                                                ).strftime("%d.%m.%Y %H:%M")
            )
        else:
            self.info_date.setText("-")

        comment = info.comment() if hasattr(info, "comment") else ""
        self.info_comment.setText(comment or "-")

        self._populate_files_tree(info)

    def _populate_files_tree(self, info):
        """Строит дерево папок и файлов из lt.torrent_info.
        Если у торрента есть общий корень — он не показывается."""
        self.files_tree.clear()
        self.files_tree.setSortingEnabled(True)
        self.files_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        storage = info.files()
        n = storage.num_files()

        folder_icon = qta.icon("fa5s.folder", color="#eab308")
        file_icon = qta.icon("fa5s.file", color="#9aa1ac")

        self._paths = []
        for i in range(n):
            full_path = storage.file_path(i).replace("\\", "/")
            self._paths.append((full_path, storage.file_size(i)))

        common_root = find_common_root([p for p, _ in self._paths])

        def strip_root(p: str) -> str:
            if not common_root:
                return p

            prefix = common_root + "/"
            return p[len(prefix):] if p.startswith(prefix) else p

        folder_nodes = {}

        for full_path, size in self._paths:
            rel_path = strip_root(full_path)
            parts = rel_path.split("/")

            parent_item = None
            current_path = ""

            for part in parts[:-1]:
                current_path = f"{current_path}/{part}" if current_path else part

                if current_path not in folder_nodes:
                    node = TorrentFileTreeItem([part, ""], True)
                    node.setIcon(0, folder_icon)
                    node.setData(0, Qt.ItemDataRole.UserRole, {"type": "folder"})

                    if parent_item is None:
                        self.files_tree.addTopLevelItem(node)
                    else:
                        parent_item.addChild(node)

                    folder_nodes[current_path] = node

                parent_item = folder_nodes[current_path]

            file_name = parts[-1]
            file_node = TorrentFileTreeItem(
                [file_name, human_size(size)], False)
            file_node.setIcon(0, file_icon)
            file_node.setData(
                0, Qt.ItemDataRole.UserRole,
                {"type": "file", "size": size}
            )
            file_node.setTextAlignment(
                1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

            if parent_item is None:
                self.files_tree.addTopLevelItem(file_node)
            else:
                parent_item.addChild(file_node)

        self._accumulate_folder_sizes(self.files_tree.invisibleRootItem())

        self.files_status.setText(
            f"Файлов: {n}, всего: {human_size(info.total_size())}"
        )

        self.files_tree.setSortingEnabled(True)
        self.files_tree.sortByColumn(1, Qt.SortOrder.DescendingOrder)

    def _accumulate_folder_sizes(self, item) -> int:
        total = 0

        for i in range(item.childCount()):
            child = item.child(i)
            data = child.data(0, Qt.ItemDataRole.UserRole) or {}

            if data.get("type") == "folder":
                size = self._accumulate_folder_sizes(child)
                child.setText(1, human_size(size))
                child.setTextAlignment(
                    1,
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                )
                total += size
            else:
                total += data.get("size", 0)

        return total

    @property
    def save_path(self) -> str:
        return self.path_edit.text().strip()

    @property
    def is_start_now(self) -> bool:
        return self.start_now_cb.isChecked()

    @property
    def is_create_folder(self) -> bool:
        return self.create_folder_cb.isChecked()

    @property
    def torrent_name(self) -> str:
        if self._torrent_info is None:
            return None

        return self.get_torrent_info.name()

    @property
    def paths(self) -> list[str]:
        if self._torrent_info is None:
            return None

        return self._paths

    @property
    def groups(self) -> list:
        return 1 #That for future

    @property
    def get_torrent_info(self):
        return self._torrent_info


class UI(QMainWindow):
    DETAILS_LEFT = [
        ("name", "Name"),
        ("size", "Size"),
        ("up_speed", "↑ Speed"),
        ("uploading", "Uploading"),
    ]
    DETAILS_MID = [
        ("status", "Status"),
        ("progress", "Progres"),
        ("given", "Given"),
        ("up_speed2", "↓ Speed"),
    ]
    DETAILS_RIGHT = [
        ("seeds", "Sids"),
        ("peers", "Pirs"),
        ("folder", "Folder"),
        ("added", "Add on"),
    ]

    INITIAL_VALUES = {
        "name": "-",
        "size": "-",
        "up_speed": "-",
        "uploading": "-",
        "status": "-",
        "progress": "-",
        "given": "-",
        "up_speed2": "-",
        "seeds": "-",
        "peers": "-",
        "folder": "-",
        "added": "-",
    }

    def __init__(self, torrent_engine):
        super().__init__()

        self.torrent_engine = torrent_engine
        self.theme = "maroon"
        self._current_selected_id = None

        self._build_ui()

    def _build_ui(self):
        """
        create main windows
        """
        self.resize(900, 600)
        self.setWindowTitle("EGBitTorrent")
        self._build_tool_bar()
        self._build_statusbar()
        self._build_central_menu()
        self._apply_theme(THEMES[self.theme])

    def _build_tool_bar(self):
        main_tool_bar = QToolBar()
        main_tool_bar.setIconSize(QSize(16, 16))
        main_tool_bar.setMovable(False)

        def tool_bar_add_action(icon_name, text, color, slot=None):
            act = QAction(qta.icon(icon_name, color=color), text, self)
            if slot:
                act.triggered.connect(slot)
            main_tool_bar.addAction(act)

            return act

        self.act_add_magnet = tool_bar_add_action(
            "fa5s.magnet", "Add by link", "#3b82f6",
            self.add_torrent_by_magnet
        )
        self.act_add_file = tool_bar_add_action(
            "fa5s.file-import", "Add by file", "#3b82f6",
            self.add_torent_by_file
        )
        self.act_resume = tool_bar_add_action(
            "fa5s.play", "Run", "#22c55e", self.run_current_torrent
        )
        self.act_pause = tool_bar_add_action(
            "fa5s.pause", "Stop", "#eab308", self.pause_current_torrent
        )
        self.act_delete = tool_bar_add_action(
            "fa5s.trash-alt", "Remove torrent", "#ef4444", self.remove_torrent
        )

        main_tool_bar.addSeparator()

        spacer = QWidget()
        spacer.setSizePolicy(spacer.sizePolicy().horizontalPolicy(),
                             spacer.sizePolicy().verticalPolicy())
        main_tool_bar.addWidget(spacer)

        self.act_theme = tool_bar_add_action(
            "fa5s.cog", "Settings", "#9aa1ac", self._toggle_theme
        )
        self.advance = tool_bar_add_action(
            "fa5s.tools", "Advance settings", "#9aa1ac"
        )
        self.statistic = tool_bar_add_action(
            "fa5s.chart-line", "Statistic", "#3b82f6"
        )
        self.info = tool_bar_add_action(
            "fa5s.info", "About", "#3b82f6"
        )

        self.addToolBar(main_tool_bar)

    def _build_central_menu(self):
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        search_bar = QWidget()
        sb_layout = QHBoxLayout(search_bar)
        sb_layout.setContentsMargins(12, 8, 12, 8)
        sb_layout.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Enter torrent name...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._apply_filter)
        self.search_edit.addAction(
            qta.icon("fa5s.search", color="#6b7280"), QLineEdit.ActionPosition.LeadingPosition
        )
        sb_layout.addWidget(self.search_edit, 1)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["All", "Downloading", "Uploading",
             "Finished", "Stopped", "Error"]
        )
        self.filter_combo.currentTextChanged.connect(self._apply_filter)
        sb_layout.addWidget(self.filter_combo)

        root.addWidget(search_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)

        self.groups_panel = self._build_group_panel()
        splitter.addWidget(self.groups_panel)

        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.setHandleWidth(1)

        self._build_table()
        right_splitter.addWidget(self.table)

        self.details = self._build_details_panel()
        right_splitter.addWidget(self.details)

        right_splitter.setStretchFactor(0, 3)
        right_splitter.setStretchFactor(1, 1)
        splitter.addWidget(right_splitter)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([220, 1060])

        root.addWidget(splitter, 1)
        self.setCentralWidget(central)

    def _add_group(self, name):
        item = QListWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)
        self.groups_list.addItem(item)

    def _build_group_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("Groups")
        title.setStyleSheet(
            "color: #6b7280; font-size: 11px; font-weight: 700; letter-spacing: 1px;"
        )
        layout.addWidget(title)

        self.groups_list = QListWidget()
        self.groups_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        layout.addWidget(self.groups_list, 1)

        add_btn = QPushButton(
            qta.icon("fa5s.plus", color="#9aa1ac"), "New group"
        )
        add_btn.setStyleSheet("text-align: left;")
        layout.addWidget(add_btn)

        return panel

    def _build_table(self):
        columns = ["Name", "Size", "Progress", "Status",
                   "Sids", "Pirs", "↓ Speed", "↑ Speed"]
        self.table = QTableWidget(0, len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(
            Qt.FocusPolicy.NoFocus)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._on_item_changed)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, len(columns)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        return self.table

    def _update_row(self, row: int, torrent: TorrentFile):
        rows_to_update = [
            (0, 'name', True),
            (1, 'byte_size', True),
            (2, 'progress', False),
            (3, 'state', True),
            (4, 'seeds', True),
            (5, 'peers', True),
            (6, 'downloading_rate', True),
            (7, 'upload_rate', True),
        ]

        self._update_row_items(row, torrent, rows_to_update)
        if torrent.state == TorrentState.ERROR:
            for c in range(8):
                item = self.table.item(row, c)
                if item:
                    item.setForeground(QColor("#ef4444"))
        else:
            for c in range(8):
                item = self.table.item(row, c)
                if item:
                    item.setForeground(QColor("#e6e8eb"))

    def _update_row_items(self, row: int, torrent: TorrentFile, rows: list):
        """
        Обновляет ячейки таблицы на основе переданного списка настроек.
        """
        text_formatters = {
            'name': lambda t: t.name,
            'byte_size': lambda t: t.size_human,
            'state': lambda t: t.state.value,
            'seeds': lambda t: self._row_seeds_element(t),
            'peers': lambda t: self._row_peers_element(t),
            'downloading_rate': lambda t: t.downloaded_rate_human,
            'upload_rate': lambda t: t.uploaded_rate_human,
        }

        for col, attr_name, update_text in rows:
            if col == 2:
                wrap = self.table.cellWidget(row, 2)
                if wrap:
                    progress_bar = wrap.findChild(QProgressBar)
                    if progress_bar:
                        progress_bar.setValue(int(torrent.progress * 100))
                
                item = self.table.item(row, 2)
                if isinstance(item, TorrentFileItem):
                    item._sort_value = torrent.progress
                continue

            item = self.table.item(row, col)
            if not isinstance(item, TorrentFileItem):
                item = TorrentFileItem("", 0)
                self.table.setItem(row, col, item)

            if update_text and attr_name in text_formatters:
                item.setText(text_formatters[attr_name](torrent))

            item._sort_value = getattr(torrent, attr_name)

            if col == 0:
                item.setData(Qt.ItemDataRole.UserRole, torrent.id)

    def _add_row(self, row: TorrentFile):
        r = self.table.rowCount()
        self.table.insertRow(r)

        name_item = TorrentFileItem(row.name, row.name)
        name_item.setData(Qt.ItemDataRole.UserRole, row.id)
        self.table.setItem(r, 0, name_item)

        self.table.setItem(r, 1, TorrentFileItem(row.size_human, row.byte_size))
        self.table.setItem(r, 2, TorrentFileItem("", row.progress))

        pb = QProgressBar()
        pb.setRange(0, 100)
        pb.setValue(int(row.progress * 100))
        pb.setTextVisible(True)
        pb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        wrap = QWidget()
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(4, 4, 4, 4) 
        wl.addWidget(pb)
        self.table.setCellWidget(r, 2, wrap)
        self.table.setItem(
            r, 3, TorrentFileItem(row.state.value, row.state.value))
        self.table.setItem(
            r, 4, TorrentFileItem(self._row_seeds_element(row), row.seeds))
        self.table.setItem(
            r, 5, TorrentFileItem(self._row_peers_element(row), row.peers))
        self.table.setItem(
            r, 6, TorrentFileItem(row.downloaded_rate_human, row.downloading_rate))
        self.table.setItem(
            r, 7, TorrentFileItem(row.uploaded_rate_human, row.upload_rate))

    def _build_info_block(self, config, values, storage):
        box = QWidget()
        vl = QVBoxLayout(box)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(4)

        for key, label_text in config:
            value = values.get(key, "-") 

            line = QLabel()
            line.setTextFormat(Qt.TextFormat.RichText)
            line.setText(f"{label_text} {value}")
            vl.addWidget(line)
            storage.append((key, label_text, line))

        return box

    def _update_details(self, torrent: TorrentFile):
        if not torrent or self.table.rowCount() == 0:
            new_values = self.INITIAL_VALUES

        else:
            new_values = {
                "name": torrent.name,
                "size": torrent.size_human,
                "up_speed": torrent.uploaded_rate_human,
                "uploading": human_size(torrent.upload_bytes),
                "status": torrent.state.value,
                "progress": str(int(torrent.progress * 100)),
                "given": human_size(torrent.downloading_bytes),
                "up_speed2": torrent.downloaded_rate_human,
                "seeds": self._row_seeds_element(torrent),
                "peers": self._row_peers_element(torrent),
                "folder": torrent.save_path,
                "added": datetime.datetime.fromtimestamp(torrent.added_at
                                                        ).strftime(
                                                            "%d.%m.%Y %H:%M"),
            }

        for label_list in (
            self.left_labels, self.mid_labels, self.right_labels):
            for key, lable_text, label_widget in label_list:
                value = new_values.get(key, "-")
                label_widget.setText(
                    f"{lable_text} {value}"
                )

    def _build_details_panel(self):
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        overview = QWidget()
        ov = QHBoxLayout(overview)
        ov.setContentsMargins(16, 12, 16, 12)
        ov.setSpacing(32)

        self.left_labels = []
        self.mid_labels = []
        self.right_labels = []

        left = self._build_info_block(
            self.DETAILS_LEFT, self.INITIAL_VALUES, self.left_labels)
        mid = self._build_info_block(
            self.DETAILS_MID, self.INITIAL_VALUES, self.mid_labels)
        right = self._build_info_block(
            self.DETAILS_RIGHT, self.INITIAL_VALUES, self.right_labels)

        ov.addWidget(left, 1)
        ov.addWidget(mid, 1)
        ov.addWidget(right, 1)

        files = QTableWidget(0, 4)
        files.setHorizontalHeaderLabels(
            ["Name", "Size", "Progres", "Priority"]
        )
        files.verticalHeader().setVisible(False)
        files.setShowGrid(False)
        files.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 4):
            files.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)

        self.tabs.addTab(overview, qta.icon("fa5s.info-circle", color="#9aa1ac"), "More")
        self.tabs.addTab(files, qta.icon("fa5s.folder-open", color="#9aa1ac"), "Files")
        return self.tabs

    def _build_statusbar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        sb.showMessage("Total: 0 │ Active: 0 │ ↓ 0 MB/s | ↑ 0 MB/s │ DHT: 0")

    def _on_item_changed(self):
        current_item = self.table.currentItem()
        if current_item is None:
            return

        torrent_id = self.table.item(current_item.row(), 0).data(
            Qt.ItemDataRole.UserRole
        )
        self._current_selected_id = torrent_id
        if not torrent_id:
            return

        torrent = self.torrent_engine.get(torrent_id)
        if torrent:
            self._update_details(torrent)

    def _get_default_savepath(self):
        return self.torrent_engine.default_savepath

    def _on_delete_clicked(self):
        torrent_id = self._get_selected_torrent_id()
        if not torrent_id:
            self._info("Select torrent.")
            return

        torrent = self.torrent_engine.get(torrent_id)
        if torrent and torrent.state == TorrentState.DOWNLOADING:
            if not self._confirm("The torrent is swinging. Stop and delete?"):
                return

        delete_files = self._confirm(
            "Should also delete the downloaded files?")

        try:
            self.torrent_engine.remove(torrent_id, delete_files=delete_files)
            self.refresh()
        except Exception as e:
            self._error("Couldn't delete", str(e))

    def _apply_filter(self):
        search_text = self.search_edit.text().strip().lower()
        filter_text = self.filter_combo.currentText()

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if not item:
                continue

            torrent_id = item.data(Qt.ItemDataRole.UserRole)
            torrent = self.torrent_engine.get(torrent_id)
            if not torrent:
                return

            match_search = search_text in torrent.name.lower()
            match_filter = (
                filter_text.upper() == torrent.state.value or
                filter_text == "All"
            )
            self.table.setRowHidden(row, not (match_filter and match_search))

    def refresh(self):
        self.table.setSortingEnabled(False)
        torrents = self.torrent_engine.get_all_torrents()
        current_ids = {torrent.id for torrent in torrents}

        for row in range(self.table.rowCount() - 1, -1, -1):
            item = self.table.item(row, 0)
            if item is None:
                continue

            torrent_id = item.data(
                Qt.ItemDataRole.UserRole)
            if torrent_id not in current_ids:
                self.table.removeRow(row)

        exists = self._index_row_by_id()
        for torrent in torrents:
            if torrent.id in exists:
                self._update_row(exists[torrent.id], torrent)
            else:
                self._add_row(torrent)

        self._update_statusbar(torrents)
        if self._current_selected_id:
            torrent = self.torrent_engine.get(self._current_selected_id)
            if torrent:
                self._update_details(torrent)
            else:
                self._current_selected_id = None
                self._update_details(None)
        else:
            if self.table.rowCount() == 0:
                self._update_details(None)

        self._apply_filter()

        self.table.setSortingEnabled(True)

    def _index_row_by_id(self):
        result = {}
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                torrent_id = item.data(Qt.ItemDataRole.UserRole)
                if torrent_id:
                    result[torrent_id] = row

        return result

    def _peers_seeds_constructor(self, attr: str, torrent: TorrentFile) -> str:
        total = getattr(torrent, attr + "_total")
        return f"{getattr(torrent, attr)} ({total if total > 0 else 0})"

    def _row_seeds_element(self, torrent: TorrentFile) -> str:
        return self._peers_seeds_constructor("seeds", torrent)

    def _row_peers_element(self, torrent: TorrentFile) -> str:
        return self._peers_seeds_constructor("peers", torrent)

    def _set_text(self, row: int, column: int, text: str):
        item = self.table.item(row, column)
        if item is None:
            self.table.setItem(row, column, QTableWidgetItem(text))

        elif item.text() != text:
            item.setText(text)

    def _update_statusbar(self, torrents):
        total = len(torrents)
        active = sum(1 for torrent in torrents if torrent.is_active)
        dlr = human_rate(sum(torrent.downloading_rate for torrent in torrents))
        ulr = human_rate(sum(torrent.upload_rate for torrent in torrents))

        self.statusBar().showMessage(
            f"Total: {total} | "
            f"Active: {active} | "
            f"↓ Downloading speed: {dlr} | "
            f"Uploading: {ulr}/s"
        )

    def add_torrent_by_magnet(self):
        magnet_window = AddMagnetWindow(self)
        result = magnet_window.exec()

        if result != QDialog.DialogCode.Accepted:
            return

        magnet_link = magnet_window.magnet_link

        validation_res = validate_magnet(magnet_link)
        if not validation_res.ok:
            self._error("Magnet link error", validation_res.error)
            return

        self._create_torrent(magnet_link, True)

    def add_torent_by_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select .torrent file", "",
            "Torrent files (*.torrent);;All files (*)"
        )

        if not path:
            return

        validate_res = validate_torrent_file(path)

        if not validate_res.ok:
            self._error(str(validate_res.error))
            return

        self._create_torrent(path)

    def _create_torrent(self, path: str, is_magnet: bool = False):
        add_torrent_window = AddTorrentWindow(
            self._get_default_savepath(), self, path, is_magnet
        )

        result = add_torrent_window.exec()
        if result != QDialog.DialogCode.Accepted:
            return

        save_path = add_torrent_window.save_path
        start_now = add_torrent_window.is_start_now
        create_folder = add_torrent_window.is_create_folder
        paths = (
            (("", 0),) if is_magnet else add_torrent_window.paths)
        torrent_name = (
            extract_magnet_name(path) if is_magnet
            else add_torrent_window.torrent_name)
        groups = add_torrent_window.groups #That for future

        validate_res = validate_save_path(save_path)
        if not validate_res.ok:
            self._error(str(validate_res.error))
            return

        save_path, is_creating = new_root_if_necessary(
            paths, save_path, torrent_name, create_folder)

        try:
            if is_creating:
                save_path = smart_folder_creating(save_path)
            if is_magnet:
                self.torrent_engine.add_magnet(
                    path, save_path, start_now
                )
            else:
                self.torrent_engine.add_torrent_file(
                    path, save_path, start_now)

            self.refresh()

        except DuplicateTorrentError as err:
            if is_creating:
                folder_remove(save_path)
            self._handle_duplicate(
                path, save_path, start_now, err.torrent_id, is_magnet)

        except Exception as e:
            if is_creating:
                folder_remove(save_path)
            self._error("Adding error", str(e))

    def _handle_duplicate(
            self, path: str, save_path: str, start_now: bool,
            torrent_id: str, is_magnet: bool):
        box = QMessageBox(self)
        box.setWindowTitle("Duplicate")
        box.setText("This torrent has already been added. What can I do?")
        box.setIcon(QMessageBox.Icon.Question)

        btn_open = box.addButton(
            "Show in list", QMessageBox.ButtonRole.AcceptRole)
        btn_new = box.addButton(
            "Download in new folder", QMessageBox.ButtonRole.ActionRole)
        btn_cancel = box.addButton(
            "Cancel", QMessageBox.ButtonRole.RejectRole)

        box.exec()

        if box.clickedButton() == btn_open:
            self._select_torrent_by_id(torrent_id)

        elif box.clickedButton() == btn_new:
            try:
                self.torrent_engine.remove(torrent_id, delete_files=False)
                self.refresh()
            except Exception as e:
                self._error("Error", f"Could not remove old torrent: {e}")
                return

            unique_path = smart_folder_creating(save_path)

            try:
                if is_magnet:
                    self.torrent_engine.add_magnet(
                        path, save_path, start_now
                    )
                else:
                    self.torrent_engine.add_torrent_file(
                        path, save_path=unique_path, start_now=start_now
                    )
                self.refresh()
            except Exception as e:
                self._error("Adding error", str(e))

    def _select_torrent_by_id(self, torrent_id: str):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is None:
                continue

            if item.data(Qt.ItemDataRole.UserRole) == torrent_id:
                self.table.selectRow(row)
                self.table.scrollToItem(item)
                return

        self._info("Torrent isn't in list.")

    def _error(self, title: str, text: str = ""):
        if text:
            QMessageBox.critical(self, title, text)
        else:
            QMessageBox.critical(self, "Error", title)

    def _info(self, text: str):
        QMessageBox.information(self, "Information", text)

    def _warn(self, text: str):
        QMessageBox.warning(self, "Warning", text)

    def _confirm(self, text: str, title: str = "Confirm") -> bool:
        answer = QMessageBox.question(
            self, title, text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return answer == QMessageBox.StandardButton.Yes

    def _manipulate_torrent(self, method: str, func: callable = None):
        current_torrents = self.table.selectedItems()
        if not current_torrents:
            return

        if func:
            result, params = func()
            if not result:
                return

        for el in current_torrents:
            if el.column() != 0:
                continue

            torrent_id = el.data(Qt.ItemDataRole.UserRole)
            if not torrent_id:
                continue

            if func and params:
                getattr(self.torrent_engine, method)(torrent_id, params)
                continue

            getattr(self.torrent_engine, method)(torrent_id)

    def run_current_torrent(self):
        self._manipulate_torrent("resume")

    def pause_current_torrent(self):
        self._manipulate_torrent("pause")

    def remove_torrent(self):
        self._manipulate_torrent(
            "remove", self._remove_torrent_window_create)

    def _remove_torrent_window_create(self) -> tuple[bool, bool]:
        remove_window = RemoveTorrent(self)
        result = remove_window.exec()

        if result != QDialog.DialogCode.Accepted:
            return (False, 0)

        return (True, remove_window.is_remove_files)

    def _apply_theme(self, theme: str):
        self.setStyleSheet(theme)

    def _toggle_theme(self):
        ...

