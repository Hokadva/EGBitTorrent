DARK_THEME = """
QWidget {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #1e1e1e; }
QGroupBox { border: 1px solid #3c3c3c; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #cccccc; }
QPushButton { background-color: #333333; border: 1px solid #555555; padding: 4px 12px; }
QPushButton:hover { background-color: #3c3c3c; border-color: #666666; }
QPushButton:pressed { background-color: #2a2a2a; }
QLineEdit, QComboBox, QSpinBox { background-color: #252526; border: 1px solid #3c3c3c; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #007acc; }
QTableView, QTreeView, QListWidget { background-color: #252526; alternate-background-color: #2d2d2d; border: 1px solid #3c3c3c; }
QHeaderView::section { background-color: #333333; border: 1px solid #3c3c3c; padding: 4px; }
QProgressBar { background-color: #252526; color: #ffffff; border: 1px solid #3c3c3c; text-align: center; }
QProgressBar::chunk { background-color: #007acc; }
QScrollBar:vertical { background: #1e1e1e; width: 14px; }
QScrollBar::handle:vertical { background: #424242; min-height: 20px; border: 1px solid #1e1e1e; }
QScrollBar::handle:vertical:hover { background: #4f4f4f; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #2d2d2d; border: 1px solid #3c3c3c; padding: 5px 10px; }
QTabBar::tab:selected { background: #1e1e1e; border-bottom: 1px solid #1e1e1e; }
QStatusBar { background: #007acc; color: #ffffff; }
"""

WHITE_THEME = """
QWidget {
    background-color: #ffffff;
    color: #333333;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #ffffff; }
QGroupBox { border: 1px solid #cccccc; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #333333; }
QPushButton { background-color: #f0f0f0; border: 1px solid #cccccc; padding: 4px 12px; }
QPushButton:hover { background-color: #e0e0e0; border-color: #adadad; }
QPushButton:pressed { background-color: #d0d0d0; }
QLineEdit, QComboBox, QSpinBox { background-color: #ffffff; border: 1px solid #cccccc; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #007acc; }
QTableView, QTreeView, QListWidget { background-color: #ffffff; alternate-background-color: #f7f7f7; border: 1px solid #cccccc; }
QHeaderView::section { background-color: #f0f0f0; border: 1px solid #cccccc; padding: 4px; }
QProgressBar { background-color: #ffffff; color: #333333; border: 1px solid #cccccc; text-align: center; color: #333333; }
QProgressBar::chunk { background-color: #007acc; }
QScrollBar:vertical { background: #ffffff; width: 14px; }
QScrollBar::handle:vertical { background: #c0c0c0; min-height: 20px; border: 1px solid #ffffff; }
QScrollBar::handle:vertical:hover { background: #a0a0a0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #f0f0f0; border: 1px solid #cccccc; padding: 5px 10px; }
QTabBar::tab:selected { background: #ffffff; border-bottom: 1px solid #ffffff; }
QStatusBar { background: #007acc; color: #ffffff; }
"""

BLACK_THEME = """
QWidget {
    background-color: #000000;
    color: #ffffff;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #000000; }
QGroupBox { border: 1px solid #333333; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #ffffff; }
QPushButton { background-color: #111111; border: 1px solid #333333; padding: 4px 12px; color: #ffffff;}
QPushButton:hover { background-color: #222222; border-color: #555555; }
QPushButton:pressed { background-color: #000000; }
QLineEdit, QComboBox, QSpinBox { background-color: #000000; border: 1px solid #333333; padding: 3px; color: #ffffff;}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #ffffff; }
QTableView, QTreeView, QListWidget { background-color: #000000; alternate-background-color: #111111; border: 1px solid #333333; }
QHeaderView::section { background-color: #111111; border: 1px solid #333333; padding: 4px; }
QProgressBar { background-color: #000000; color: #ffffff;  border: 1px solid #333333; text-align: center; }
QProgressBar::chunk { background-color: #ffffff; }
QScrollBar:vertical { background: #000000; width: 14px; }
QScrollBar::handle:vertical { background: #333333; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #555555; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #111111; border: 1px solid #333333; padding: 5px 10px; color: #ffffff;}
QTabBar::tab:selected { background: #000000; border-bottom: 1px solid #000000; }
QStatusBar { background: #111111; color: #ffffff; border-top: 1px solid #333333; }
"""

BLACK_BLUE_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #2b2b2b; }
QGroupBox { border: 1px solid #444444; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #3daee9; }
QPushButton { background-color: #3c3c3c; border: 1px solid #555555; padding: 4px 12px; }
QPushButton:hover { background-color: #4a4a4a; border-color: #3daee9; }
QPushButton:pressed { background-color: #2a2a2a; }
QLineEdit, QComboBox, QSpinBox { background-color: #2b2b2b; border: 1px solid #444444; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #3daee9; }
QTableView, QTreeView, QListWidget { background-color: #2b2b2b; alternate-background-color: #323232; border: 1px solid #444444; }
QHeaderView::section { background-color: #3c3c3c; border: 1px solid #444444; padding: 4px; }
QProgressBar { background-color: #2b2b2b; olor: #e0e0e0; border: 1px solid #444444; text-align: center; }
QProgressBar::chunk { background-color: #3daee9; }
QScrollBar:vertical { background: #2b2b2b; width: 14px; }
QScrollBar::handle:vertical { background: #555555; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #3daee9; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #323232; border: 1px solid #444444; padding: 5px 10px; }
QTabBar::tab:selected { background: #2b2b2b; border-bottom: 1px solid #2b2b2b; }
QStatusBar { background: #3daee9; color: #ffffff; }
"""

BLACK_RED_THEME = """
QWidget {
    background-color: #222222;
    color: #f8f8f2;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #222222; }
QGroupBox { border: 1px solid #444444; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #ff5555; }
QPushButton { background-color: #333333; border: 1px solid #555555; padding: 4px 12px; }
QPushButton:hover { background-color: #444444; border-color: #ff5555; }
QPushButton:pressed { background-color: #111111; }
QLineEdit, QComboBox, QSpinBox { background-color: #1e1e1e; border: 1px solid #444444; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #ff5555; }
QTableView, QTreeView, QListWidget { background-color: #1e1e1e; alternate-background-color: #222222; border: 1px solid #444444; }
QHeaderView::section { background-color: #333333; border: 1px solid #444444; padding: 4px; }
QProgressBar { background-color: #1e1e1e; color: #f8f8f2; border: 1px solid #444444; text-align: center; }
QProgressBar::chunk { background-color: #ff5555; }
QScrollBar:vertical { background: #1e1e1e; width: 14px; }
QScrollBar::handle:vertical { background: #444444; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #ff5555; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #333333; border: 1px solid #444444; padding: 5px 10px; }
QTabBar::tab:selected { background: #222222; border-bottom: 1px solid #222222; }
QStatusBar { background: #333333; color: #f8f8f2; border-top: 1px solid #ff5555; }
"""

MARIN_ORANGE_THEME = """
QWidget {
    background-color: #002b36;
    color: #839496;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #002b36; }
QGroupBox { border: 1px solid #073642; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #cb4b16; }
QPushButton { background-color: #073642; border: 1px solid #586e75; padding: 4px 12px; color: #839496;}
QPushButton:hover { background-color: #0a4452; border-color: #cb4b16; }
QPushButton:pressed { background-color: #002b36; }
QLineEdit, QComboBox, QSpinBox { background-color: #002b36; border: 1px solid #073642; padding: 3px; color: #839496;}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #cb4b16; }
QTableView, QTreeView, QListWidget { background-color: #002b36; alternate-background-color: #073642; border: 1px solid #073642; }
QHeaderView::section { background-color: #073642; border: 1px solid #002b36; padding: 4px; }
QProgressBar { background-color: #002b36; color: #839496; border: 1px solid #073642; text-align: center; }
QProgressBar::chunk { background-color: #cb4b16; }
QScrollBar:vertical { background: #002b36; width: 14px; }
QScrollBar::handle:vertical { background: #073642; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #cb4b16; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #073642; border: 1px solid #002b36; padding: 5px 10px; color: #839496;}
QTabBar::tab:selected { background: #002b36; border-bottom: 1px solid #002b36; }
QStatusBar { background: #073642; color: #839496; }
"""

WHITE_RED_THEME = """
QWidget {
    background-color: #f5f5f5;
    color: #333333;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #f5f5f5; }
QGroupBox { border: 1px solid #cccccc; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #cc0000; }
QPushButton { background-color: #e0e0e0; border: 1px solid #cccccc; padding: 4px 12px; }
QPushButton:hover { background-color: #d0d0d0; border-color: #cc0000; }
QPushButton:pressed { background-color: #c0c0c0; }
QLineEdit, QComboBox, QSpinBox { background-color: #ffffff; border: 1px solid #cccccc; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #cc0000; }
QTableView, QTreeView, QListWidget { background-color: #ffffff; alternate-background-color: #f9f9f9; border: 1px solid #cccccc; }
QHeaderView::section { background-color: #e0e0e0; border: 1px solid #cccccc; padding: 4px; }
QProgressBar { background-color: #ffffff; color: #333333; border: 1px solid #cccccc; text-align: center; color: #333333;}
QProgressBar::chunk { background-color: #cc0000; }
QScrollBar:vertical { background: #f5f5f5; width: 14px; }
QScrollBar::handle:vertical { background: #c0c0c0; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #cc0000; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #e0e0e0; border: 1px solid #cccccc; padding: 5px 10px; }
QTabBar::tab:selected { background: #ffffff; border-bottom: 1px solid #ffffff; }
QStatusBar { background: #cc0000; color: #ffffff; }
"""

WHITE_BLUE_THEME = """
QWidget {
    background-color: #ffffff;
    color: #333333;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #ffffff; }
QGroupBox { border: 1px solid #cccccc; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #0066cc; }
QPushButton { background-color: #f0f0f0; border: 1px solid #cccccc; padding: 4px 12px; }
QPushButton:hover { background-color: #e0e0e0; border-color: #0066cc; }
QPushButton:pressed { background-color: #d0d0d0; }
QLineEdit, QComboBox, QSpinBox { background-color: #ffffff; border: 1px solid #cccccc; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #0066cc; }
QTableView, QTreeView, QListWidget { background-color: #ffffff; alternate-background-color: #f7f7f7; border: 1px solid #cccccc; }
QHeaderView::section { background-color: #f0f0f0; border: 1px solid #cccccc; padding: 4px; }
QProgressBar { background-color: #ffffff; color: #333333; border: 1px solid #cccccc; text-align: center; color: #333333;}
QProgressBar::chunk { background-color: #0066cc; }
QScrollBar:vertical { background: #ffffff; width: 14px; }
QScrollBar::handle:vertical { background: #c0c0c0; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #0066cc; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #f0f0f0; border: 1px solid #cccccc; padding: 5px 10px; }
QTabBar::tab:selected { background: #ffffff; border-bottom: 1px solid #ffffff; }
QStatusBar { background: #0066cc; color: #ffffff; }
"""

MAROON_THEME = """
QWidget {
    background-color: #1a1c20;
    color: #e2ded4;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QMainWindow, QDialog { background-color: #1a1c20; }
QGroupBox { border: 1px solid #3c3c3c; margin-top: 12px; padding-top: 12px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #c83a3a; }
QPushButton { background-color: #2b2e35; border: 1px solid #444444; padding: 4px 12px; }
QPushButton:hover { background-color: #383c45; border-color: #c83a3a; }
QPushButton:pressed { background-color: #1a1c20; }
QLineEdit, QComboBox, QSpinBox { background-color: #252526; border: 1px solid #444444; padding: 3px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #c83a3a; }
QTableView, QTreeView, QListWidget { background-color: #252526; alternate-background-color: #2d2d2d; border: 1px solid #444444; }
QHeaderView::section { background-color: #2b2e35; border: 1px solid #444444; padding: 4px; }
QProgressBar { background-color: #252526; color: #e2ded4; border: 1px solid #444444; text-align: center; }
QProgressBar::chunk { background-color: #c83a3a; }
QScrollBar:vertical { background: #1a1c20; width: 14px; }
QScrollBar::handle:vertical { background: #444444; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #c83a3a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabBar::tab { background: #2b2e35; border: 1px solid #444444; padding: 5px 10px; }
QTabBar::tab:selected { background: #1a1c20; border-bottom: 1px solid #1a1c20; }
QStatusBar { background: #2b2e35; color: #e2ded4; border-top: 1px solid #c83a3a; }
"""

THEMES = {
    "dark": DARK_THEME,
    "black": BLACK_THEME,
    "white": WHITE_THEME,
    "black_red": BLACK_RED_THEME,
    "black_blue": BLACK_BLUE_THEME,
    "white_red": WHITE_RED_THEME,
    "white_blue": WHITE_BLUE_THEME,
    "marin_orange": MARIN_ORANGE_THEME,
    "maroon": MAROON_THEME
}