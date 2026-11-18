BASE_TEMPLATE = """
QWidget {{
    background-color: {bg_main};
    color: {text_main};
    font-family: "Segoe UI", sans-serif;
}}
QMainWindow, QDialog {{ background-color: {bg_main}; }}
QGroupBox {{ border: 1px solid {border}; margin-top: 12px; padding-top: 12px; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 8px; padding: 0 3px; color: {text_main}; }}
QPushButton {{ 
    background-color: {bg_btn}; 
    border: 1px solid {border}; 
    padding: 4px 12px; 
    color: {text_main};
}}
QPushButton:hover {{ background-color: {bg_hover}; border-color: {accent}; }}
QPushButton:pressed {{ background-color: {bg_main}; }}
QLineEdit, QComboBox, QSpinBox {{ 
    background-color: {bg_input}; 
    border: 1px solid {border}; 
    padding: 3px; 
    color: {text_main};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{ border: 1px solid {accent}; }}
QTableView, QTreeView, QListWidget {{ 
    background-color: {bg_input}; 
    alternate-background-color: {bg_alt}; 
    border: 1px solid {border}; 
    color: {text_main};
}}
QHeaderView::section {{ 
    background-color: {bg_btn}; 
    border: 1px solid {border}; 
    padding: 4px; 
    color: {text_main};
}}
QProgressBar {{ 
    background-color: {bg_input}; 
    color: {text_main}; 
    border: 1px solid {border}; 
    text-align: center; 
}}
QProgressBar::chunk {{ background-color: {accent}; }}
QScrollBar:vertical {{ background: {bg_main}; width: 14px; }}
QScrollBar::handle:vertical {{ background: {border}; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: {accent}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
QTabBar::tab {{ background: {bg_btn}; border: 1px solid {border}; padding: 5px 10px; color: {text_main}; }}
QTabBar::tab:selected {{ background: {bg_main}; border-bottom: 1px solid {bg_main}; }}
QStatusBar {{ background: {accent}; color: {text_status}; }}
QComboBox QAbstractItemView {{ font-size: 12px; }}
QComboBox QAbstractItemView::item {{ font-size: 12px; }}
QTableView::item:selected, QTreeView::item:selected, QListWidget::item:selected {{
    background-color: {accent};
    color: {text_main};
}}
QTableView::item:hover, QTreeView::item:hover, QListWidget::item:hover {{
    background-color: {bg_hover};
}}
"""

THEMES_DATA = {
    "dark": {
        "bg_main": "#1e1e1e", "bg_btn": "#333333", "bg_hover": "#3c3c3c",
        "bg_input": "#252526", "bg_alt": "#2d2d2d", "text_main": "#cccccc",
        "border": "#3c3c3c", "accent": "#007acc", "text_status": "#ffffff"
    },
    "white": {
        "bg_main": "#ffffff", "bg_btn": "#f0f0f0", "bg_hover": "#e0e0e0",
        "bg_input": "#ffffff", "bg_alt": "#f7f7f7", "text_main": "#333333",
        "border": "#cccccc", "accent": "#007acc", "text_status": "#ffffff",
        "text_main": "#333333"
    },
    "black": {
        "bg_main": "#000000", "bg_btn": "#111111", "bg_hover": "#222222",
        "bg_input": "#000000", "bg_alt": "#111111", "text_main": "#ffffff",
        "border": "#333333", "accent": "#ffffff", "text_status": "#000000",
        "text_main": "#e2ded4"
    },
    "black_blue": {
        "bg_main": "#2b2b2b", "bg_btn": "#3c3c3c", "bg_hover": "#4a4a4a",
        "bg_input": "#2b2b2b", "bg_alt": "#323232", "text_main": "#e0e0e0",
        "border": "#444444", "accent": "#3daee9", "text_status": "#ffffff",
        "text_main": "#e2ded4"
    },
    "black_red": {
        "bg_main": "#222222", "bg_btn": "#333333", "bg_hover": "#444444",
        "bg_input": "#1e1e1e", "bg_alt": "#222222", "text_main": "#f8f8f2",
        "border": "#444444", "accent": "#e05454", "text_status": "#f8f8f2",
        "text_main": "#e2ded4"
    },
    "marin_orange": {
        "bg_main": "#002b36", "bg_btn": "#073642", "bg_hover": "#0a4452",
        "bg_input": "#002b36", "bg_alt": "#073642", "text_main": "#839496",
        "border": "#073642", "accent": "#cb4b16", "text_status": "#839496",
        "text_main": "#e2ded4"
    },
    "white_red": {
        "bg_main": "#f5f5f5", "bg_btn": "#e0e0e0", "bg_hover": "#d0d0d0",
        "bg_input": "#ffffff", "bg_alt": "#f9f9f9", "text_main": "#333333",
        "border": "#cccccc", "accent": "#e05454", "text_status": "#ffffff",
        "text_main": "#333333"
    },
    "white_blue": {
        "bg_main": "#ffffff", "bg_btn": "#f0f0f0", "bg_hover": "#e0e0e0",
        "bg_input": "#ffffff", "bg_alt": "#f7f7f7", "text_main": "#333333",
        "border": "#cccccc", "accent": "#0066cc", "text_status": "#ffffff",
        "text_main": "#333333"
    },
    "maroon": {
        "bg_main": "#1a1c20", "bg_btn": "#2b2e35", "bg_hover": "#383c45",
        "bg_input": "#252526", "bg_alt": "#2d2d2d", "text_main": "#e2ded4",
        "border": "#444444", "accent": "#c83a3a", "text_status": "#e2ded4",
        "text_main": "#e2ded4"
    }
}

THEMES = {}
for name, colors in THEMES_DATA.items():
    THEMES[name] = BASE_TEMPLATE.format(**colors)
