from enum import Enum
import os


class ToolBarColors(Enum):
    BASE = "#3b82f6"
    GREEN = "#22c55e"
    YELLOW = "#eab308"
    RED = "#ef4444"
    GRAY = "#9aa1ac"


class AppColors(Enum):
    GRAY = "#6b7280"
    RED = "#ef4444"
    WHITE = "#e6e8eb"
    GREEN = "#22c55e"
    YELLOW = "#eab308"
    DARK_GREY = "#6b7280"


class SettingsParametrs(Enum):
    LANGUAGE = "language"
    THEME = "theme"
    BASE_SAVE_PATH = "base_save_path"
    DOWNLOADS_LIMIT = "downloads_limit"
    UPLOAD_SPEED_LIMIT = "upload_speed_limit"
    DOWNLOAD_SPEED_LIMIT = "download_speed_limit"


VERSION = 1.0
DEFAULT_THEME = "maroon"
APP_NAME = "EGBitTorrent"

SETTINGS_PATH = "data/settings.json"
DATABASE_PATH = "data/history.db"

LANGUAGES = ["ru", "en", "sp"]
