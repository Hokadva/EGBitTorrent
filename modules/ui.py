from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QToolBar, QLineEdit, QComboBox, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar,
    QListWidget, QListWidgetItem, QTabWidget, QStatusBar,
    QHeaderView, QAbstractItemView, QFileDialog, QMessageBox, QDialog,
    QDialogButtonBox, QGroupBox, QCheckBox, QGridLayout
)
from modules.torrent import TorrentFile
from PyQt6.QtGui import QAction, QIcon
import qtawesome as qta
from modules.themes import DARK_QSS
from modules.validator import (
    validate_save_path, validate_add_magnet, validate_add_file
)
from modules.core import human_size, get_free_disk_space


class AddTorrentWindow(QDialog):
    MODE_MAGNET = "magnet"
    MODE_FILE = "file"

    def __init__(self, default_save_path: str, mode: str, parent):
        super().__init__(parent)

        if mode not in (self.MODE_MAGNET, self.MODE_FILE):
            raise ValueError("Incorrect mode")

        self.setWindowTitle("Add torrent")
        self.resize(820, 560)

        self._default_save_path = default_save_path

        self.build_ui()
        self._validate()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(12)

        top.addWidget(self._build_left_panel(), 1)
        top.addWidget(self._build_right_panel(), 1)

        root.addLayout(top, 1)

        root.addWidget(self._build_bottom_panel())

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Add")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        self._button_box = buttons

    def _build_left_panel(self):
        panel = QVBoxLayout()
        panel.setSpacing(10)

        if self.mode == self.MODE_MAGNET:
            source_group = QGroupBox("Magnet-link")
            sg = QVBoxLayout(source_group)

            self.magnet_edit = QLineEdit()
            self.magnet_edit.setPlaceholderText("magnet:?xt=urn:btih:...")
            self.magnet_edit.textChanged.connect(self._validate)
            sg.addWidget(self.magnet_edit)

        else:
            source_group = QGroupBox(".torrent-file")
            sg = QVBoxLayout(source_group)

            row = QHBoxLayout()
            row.setSpacing(6)

            self.file_edit = QLineEdit()
            self.file_edit.setPlaceholderText("Torrent-file path...")
            self.file_edit.textChanged.connect(self._validate)
            row.addWidget(self.file_edit, 1)

            browse_file_btn = QPushButton(
                qta.icon("fa5s.file-import", color="#9aa1ac"), ""
            )
            browse_file_btn.setFixedWidth(34)
            browse_file_btn.clicked.connect(self._on_browse_file)
            row.addWidget(browse_file_btn)

            sg.addLayout(row)

        panel.addWidget(source_group)

        save_group = QGroupBox("Save folder")
        svg = QVBoxLayout(save_group)

        row = QHBoxLayout()
        row.setSpacing(6)

        self.path_edit = QLineEdit(self._default_save_path)
        self.path_edit.textChanged.connect(self._update_free_space)
        row.addWidget(self.path_edit, 1)

        browse_dir_btn = QPushButton(
            qta.icon("fa5s.folder-open", color="#9aa1ac"), ""
        )
        browse_dir_btn.setFixedWidth(34)
        browse_dir_btn.clicked.connect(self._on_browse_dir)
        row.addWidget(browse_dir_btn)

        svg.addLayout(row)

        self.free_space_label = QLabel("Free disc-space: -")
        self.free_space_label.setStyleSheet("color: #9aa1ac; font-size: 11px;")
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

        panel.addStretch(1)

        return panel

    def _build_right_panel(self):
        panel = QVBoxLayout()
        panel.setSpacing(10)

        files_group = QGroupBox("Files:")
        fg = QVBoxLayout(files_group)

        self.files_table = QTableWidget(0, 2)
        self.files_table.setHorizontalHeaderLabels(["Name", "Size"])
        self.files_table.verticalHeader().setVisible(False)
        self.files_table.setShowGrid(False)
        self.files_table.setAlternatingRowColors(True)
        self.files_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.files_table.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)

        header = self.files_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents)

        fg.addWidget(self.files_table)

        self.files_status = QLabel("—")
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

        self.info_name = QLabel("—")
        add_row(0, "Name", self.info_name)

        self.info_size = QLabel("—")
        self.info_date = QLabel("—")
        row1 = QHBoxLayout()
        row1.setSpacing(24)
        row1.addWidget(QLabel("Size:"))
        row1.addWidget(self.info_size)
        row1.addSpacing(20)
        row1.addWidget(QLabel("Date of creation:"))
        row1.addWidget(self.info_date)
        row1.addStretch(1)
        grid.addLayout(row1, 1, 1, 1, 3)

        self.info_comment = QLabel("—")
        self.info_comment.setWordWrap(True)
        add_row(2, "Comment:", self.info_comment)

        return box

    def _on_browse_file(self):
        path, _ = QFileDialog.getOpe


class UI(QMainWindow):
    def __init__(self, torrent_engine):
        super().__init__()

        self.torrent_engine = torrent_engine
        self.theme = "dark"

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
            "fa5s.magnet", "Add by link", "#3b82f6"
        )
        self.act_add_file = tool_bar_add_action(
            "fa5s.file-import", "Add by file", "#3b82f6",
            self.add_torent_by_file
        )
        self.act_resume = tool_bar_add_action(
            "fa5s.play", "Run", "#22c55e"
        )
        self.act_pause = tool_bar_add_action(
            "fa5s.pause", "Stop", "#eab308"
        )
        self.act_delete = tool_bar_add_action(
            "fa5s.trash-alt", "Remove torrent", "#ef4444"
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
        search_bar.setStyleSheet("background-color: #20242b;")
        sb_layout = QHBoxLayout(search_bar)
        sb_layout.setContentsMargins(12, 8, 12, 8)
        sb_layout.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Enter torrent name...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.addAction(
            qta.icon("fa5s.search", color="#6b7280"), QLineEdit.ActionPosition.LeadingPosition
        )
        sb_layout.addWidget(self.search_edit, 1)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["All", "Downloading", "Uploading",
             "Finished", "Stopped", "Error"]
        )
        sb_layout.addWidget(self.filter_combo)

        root.addWidget(search_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)

        self.groups_panel = self._build_group_panel()
        splitter.addWidget(self.groups_panel)

        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.setHandleWidth(1)

        self.table = self._build_table()
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

        for name in ["All", "Films", "Music", "Work", "Others"]:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.groups_list.addItem(item)

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
        table = QTableWidget(0, len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        header = table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, len(columns)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        return table

    def _update_row(self, row: int, torrent: TorrentFile):
        name_item = self.table.item(row, 0)

        self._set_text(row, 0, torrent.name)

        name_item.setData(Qt.ItemDataRole.UserRole, torrent.id)

        self._set_text(row, 1, torrent.size_human)

        wrap = self.table.cellWidget(row, 2)
        if wrap:
            progress_bar = wrap.findChild(QProgressBar)
            if progress_bar:
                progress_bar.setValue(int(torrent.progress * 100))

        state_item = self.table.item(row, 3)
        state_text = torrent.state.value
        if state_item.text() != state_item:
            state_item.setText(state_text)

        self._set_text(row, 4, self._row_seeds_element(torrent))
        self._set_text(row, 5, self._row_peers_element(torrent))

        self._set_text(row, 6, torrent.downloaded_rate_human)
        self._set_text(row, 7, torrent.uploaded_rate_human)

    def _add_row(self, row: TorrentFile):
        r = self.table.rowCount()
        self.table.insertRow(r)

        name_item = QTableWidgetItem(row.name)
        name_item.setData(Qt.ItemDataRole.UserRole, row.id)
        self.table.setItem(r, 0, name_item)

        self.table.setItem(r, 1, QTableWidgetItem(row.size_human))

        pb = QProgressBar()
        pb.setRange(0, 100)
        pb.setValue(int(row.progress * 1000))
        pb.setTextVisible(False)
        pb.setFixedHeight(6)
        wrap = QWidget()
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(6, 10, 6, 10)
        wl.addWidget(pb)
        self.table.setCellWidget(r, 2, wrap)

        self.table.setItem(r, 3, QTableWidgetItem(row.state.value))
        self.table.setItem(r, 4, QTableWidgetItem(self._row_seeds_element(row)))
        self.table.setItem(r, 5, QTableWidgetItem(self._row_peers_element(row)))
        self.table.setItem(r, 6, QTableWidgetItem(row.downloaded_rate_human))
        self.table.setItem(r, 7, QTableWidgetItem(row.uploaded_rate_human))

    def _build_details_panel(self):
        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        overview = QWidget()
        ov = QHBoxLayout(overview)
        ov.setContentsMargins(16, 12, 16, 12)
        ov.setSpacing(32)

        def info_block(items):
            box = QWidget()
            vl = QVBoxLayout(box)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.setSpacing(4)
            for label, value in items:
                line = QLabel(f"<span style='color:#6b7280'>{label}:</span> "
                              f"<span style='color:#e6e8eb'>{value}</span>")
                vl.addWidget(line)
            return box

        left = info_block([
            ("Name", ""),
            ("Size", ""),
            ("↑ Speed", ""),
            ("Uploading", ""),
        ])
        mid = info_block([
            ("Status", ""),
            ("Progres", ""),
            ("Given", ""),
            ("↑ Speed", ""),
        ])
        right = info_block([
            ("Sids", ""),
            ("Pirs", ""),
            ("Folder", ""),
            ("Add on", ""),
        ])
        ov.addWidget(left, 1)
        ov.addWidget(mid, 1)
        ov.addWidget(right, 1)

        files = QTableWidget(0, 4)
        files.setHorizontalHeaderLabels(
            ["Name", "Size", "Progres", "Priority"]
        )
        files.verticalHeader().setVisible(False)
        files.setShowGrid(False)
        files.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 4):
            files.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        tabs.addTab(overview, qta.icon("fa5s.info-circle", color="#9aa1ac"), "More")
        tabs.addTab(files, qta.icon("fa5s.folder-open", color="#9aa1ac"), "Files")
        return tabs

    def _build_statusbar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        sb.showMessage("Total: 0 │ Active: 0 │ ↓ 0 MB/s | ↑ 0 MB/s │ DHT: 0")

    def _get_default_savepath(self):
        return self.torrent_engine.default_savepath

    def refresh(self):
        torrents = self.torrent_engine.get_all_torrents()
        current_ids = {torrent.id for torrent in torrents}

        for row in range(self.table.rowCount() - 1, -1, -1):
            item = self.table.item(row, 0)
            if item is None:
                continue

            torrent_id = item.data(Qt.ItemDataRole.UserRole)
            if torrent_id not in current_ids:
                self.table.removeRow(row)

        exists = self._index_row_by_id()
        for torrent in torrents:
            if torrent.id in exists:
                self._update_row(exists[torrent.id], torrent)
            else:
                self._add_row(self.table, torrent)

        self._update_statusbar(torrents)

    def _index_row_by_id(self):
        result = {}
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                torrent_id = item.data(Qt.ItemDataRole.UserRole)
                if torrent_id:
                    result[torrent_id] = row

        return result

    def _row_seeds_element(self, torrent):
        return f"{torrent.seeds} ({torrent.seeds_total if torrent.seeds_total > 0 else 0})"

    def _row_peers_element(self, torrent):
        return f"{torrent.peers} ({torrent.peers_total if torrent.peers_total > 0 else 0})"

    def _set_text(self, row: int, column: int, text: str):
        item = self.table.item(row, column)
        if item is None:
            self.table.setItem(row, column, QTableWidgetItem(text))

        elif item.text() != text:
            item.setText(text)

    def _update_statusbar(self, torrents):
        total = len(torrents)
        active = sum(1 for torrent in torrents if torrent.is_active)
        dlr = sum(torrent.downloading_rate for torrent in torrents)
        ulr = sum(torrent.upload_rate for torrent in torrents)

        self.statusBar().showMessage(
            f"Total: {total} | "
            f"Active: {active} | "
            f"↓ Downloading speed: {dlr}/s | "
            f"Uploading: {ulr}/s"
        )

    def add_torent_by_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select .torrent file", "",
            "Torrent files (*.torrent);;All files (*)"
        )

        if not path:
            return

        validate_res = validate_add_file(
            path, self._get_default_savepath(), False
        )

        if not validate_res.ok:
            QMessageBox.critical(
                self, "Error", f"{validate_res.error}"
            )
            return

        self._add_torrent_window(self, path)

    def _add_torrent_window(self, path):
        ...

    def _apply_theme(self):
        ...

    def _toggle_theme(self):
        ...

