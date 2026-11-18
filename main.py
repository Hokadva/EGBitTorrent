import libtorrent as lt #Don't touch if we will import lb after PyQT6 we will catch
#Segmentation fault, why? idk that very stupid, but that all what i can do
from modules.ui import UI
import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from modules.torrent_engine import TorrentEngine
from modules.models import TorrentModel
from modules.core import get_default_save_path
from modules.consts import DATABASE_PATH, SETTINGS_PATH
from modules.settings_manager import SettingManager
import os

def main():
    application = QApplication(sys.argv)

    db = TorrentModel(DATABASE_PATH)
    settings_manager = SettingManager(SETTINGS_PATH)

    torrent_engine = TorrentEngine(
        default_save_path=get_default_save_path(),
        max_active=3, db=db
    )
    torrent_engine.restore()

    main_window = UI(torrent_engine, db, settings_manager=settings_manager)

    timer = QTimer()
    timer.timeout.connect(torrent_engine.update)
    timer.timeout.connect(main_window.refresh)
    timer.start(1000)

    main_window.show()
    application.aboutToQuit.connect(torrent_engine.shutdown)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
