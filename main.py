import libtorrent as lt #Don't touch if we will import lb after PyQT6 we will catch
#Segmentation fault, why? idk that very stupid, but that all what i can do
from modules.ui import UI
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from modules.torrent_engine import TorrentEngine
import os


def main():
    application = QApplication(sys.argv)
    
    torrent_engine = TorrentEngine(
        default_save_path=os.path.expanduser("~/Downloads"),
        max_active=3
    )

    main_window = UI(torrent_engine)

    timer = QTimer()
    timer.timeout.connect(torrent_engine.update)
    timer.timeout.connect(main_window.refresh)
    timer.start(1000)

    main_window.show()
    application.aboutToQuit.connect(torrent_engine.shutdown)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
