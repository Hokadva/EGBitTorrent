DARK_QSS = """
QWidget {
    background-color: #1a1d23;
    color: #e6e8eb;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

/* Главное окно */
QMainWindow, QDialog {
    background-color: #1a1d23;
}

/* Toolbar */
QToolBar {
    background-color: #20242b;
    border: none;
    padding: 6px 8px;
    spacing: 6px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 12px;
    color: #e6e8eb;
}
QToolButton:hover {
    background-color: #2a2f38;
    border-color: #343a45;
}
QToolButton:pressed {
    background-color: #343a45;
}
QToolButton:disabled {
    color: #5a6068;
}

/* Кнопки */
QPushButton {
    background-color: #2a2f38;
    border: 1px solid #343a45;
    border-radius: 6px;
    padding: 6px 14px;
    color: #e6e8eb;
}
QPushButton:hover { background-color: #343a45; }
QPushButton:pressed { background-color: #3d444f; }
QPushButton:disabled { color: #5a6068; background-color: #23272e; }

/* Поля ввода */
QLineEdit {
    background-color: #20242b;
    border: 1px solid #343a45;
    border-radius: 6px;
    padding: 6px 10px;
    color: #e6e8eb;
    selection-background-color: #3b82f6;
}
QLineEdit:focus {
    border-color: #3b82f6;
}

/* Таблица */
QTableView {
    background-color: #1a1d23;
    alternate-background-color: #1e2228;
    gridline-color: #262b33;
    border: none;
    selection-background-color: #2a3a55;
    selection-color: #e6e8eb;
}
QHeaderView::section {
    background-color: #20242b;
    color: #9aa1ac;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid #2a2f38;
    font-weight: 600;
    font-size: 12px;
}
QTableView::item {
    padding: 6px 10px;
    border: none;
}
QTableView::item:selected {
    background-color: #2a3a55;
}

/* Прогресс-бар */
QProgressBar {
    background-color: #20242b;
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 4px;
}

/* Левая панель */
QListWidget {
    background-color: #20242b;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 4px;
}
QListWidget::item:hover { background-color: #2a2f38; }
QListWidget::item:selected { background-color: #2a3a55; }

/* Скроллбары */
QScrollBar:vertical {
    background: #1a1d23;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #343a45;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #3d444f; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QScrollBar:horizontal {
    background: #1a1d23;
    height: 10px;
}
QScrollBar::handle:horizontal {
    background: #343a45;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* Вкладки */
QTabWidget::pane {
    border: none;
    background-color: #1a1d23;
}
QTabBar::tab {
    background-color: transparent;
    color: #9aa1ac;
    padding: 6px 14px;
    margin-right: 4px;
    border-radius: 6px;
}
QTabBar::tab:hover { background-color: #2a2f38; color: #e6e8eb; }
QTabBar::tab:selected { background-color: #2a2f38; color: #e6e8eb; }

/* Статус-бар */
QStatusBar {
    background-color: #20242b;
    color: #9aa1ac;
    border-top: 1px solid #2a2f38;
}
QStatusBar::item { border: none; }

/* Чекбоксы */
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1px solid #343a45;
    background-color: #20242b;
}
QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
}

/* Меню */
QMenu {
    background-color: #20242b;
    border: 1px solid #2a2f38;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected { background-color: #2a3a55; }
"""


LIGHT_QSS = """
QWidget {
    background-color: #f7f8fa;
    color: #1a1d23;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}
QMainWindow, QDialog { background-color: #f7f8fa; }
QToolBar { background-color: #ffffff; border: none; padding: 6px 8px; spacing: 6px; }
QToolButton {
    background-color: transparent; border: 1px solid transparent;
    border-radius: 6px; padding: 6px 12px; color: #1a1d23;
}
QToolButton:hover { background-color: #eef0f3; border-color: #e0e3e8; }
QToolButton:pressed { background-color: #e0e3e8; }
QPushButton {
    background-color: #ffffff; border: 1px solid #e0e3e8;
    border-radius: 6px; padding: 6px 14px; color: #1a1d23;
}
QPushButton:hover { background-color: #eef0f3; }
QLineEdit {
    background-color: #ffffff; border: 1px solid #e0e3e8;
    border-radius: 6px; padding: 6px 10px; color: #1a1d23;
}
QLineEdit:focus { border-color: #3b82f6; }
QTableView {
    background-color: #ffffff; alternate-background-color: #f7f8fa;
    gridline-color: #eef0f3; border: none;
    selection-background-color: #dbeafe; selection-color: #1a1d23;
}
QHeaderView::section {
    background-color: #ffffff; color: #6b7280;
    padding: 8px 10px; border: none;
    border-bottom: 1px solid #e0e3e8; font-weight: 600; font-size: 12px;
}
QProgressBar { background-color: #eef0f3; border: none; border-radius: 4px; height: 6px; }
QProgressBar::chunk { background-color: #3b82f6; border-radius: 4px; }
QListWidget { background-color: #ffffff; border: none; }
QListWidget::item { padding: 6px 8px; border-radius: 4px; }
QListWidget::item:hover { background-color: #eef0f3; }
QListWidget::item:selected { background-color: #dbeafe; }
QTabBar::tab { padding: 6px 14px; color: #6b7280; }
QTabBar::tab:selected { background-color: #eef0f3; color: #1a1d23; border-radius: 6px; }
QStatusBar { background-color: #ffffff; color: #6b7280; border-top: 1px solid #e0e3e8; }
"""



