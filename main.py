import libtorrent as lt #Don't touch if we will import lb after PyQT6 we will catch
#Segmentation fault, why? idk that very stupid, but that all what i can do
from modules.ui import UI
import sys
import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from modules.torrent_engine import TorrentEngine
from modules.models import TorrentModel
from PyQt6.QtCore import QRunnable, QThreadPool
import os


class SaveHistoryTask(QRunnable):
    def __init__(self, db, torrent, status, finished_iso, removed_iso, added_iso):
        super().__init__()
        self.db = db
        self.torrent = torrent
        self.status = status
        self.finished_iso = finished_iso
        self.removed_iso = removed_iso
        self.added_iso = added_iso

    def run(self):
        self.db.add_history_record(
            torrent_id=self.torrent.id,
            name=self.torrent.name,
            size_bytes=self.torrent.byte_size,
            save_path=self.torrent.save_path,
            added_at=self.added_iso,
            status=self.status,
            finished_at=self.finished_iso,
            removed_at=self.removed_iso,
            error_message=self.torrent.error_message
        )



def main():
    thread_pool = QThreadPool.globalInstance()
    application = QApplication(sys.argv)

    db = TorrentModel("data/history.db")

    def save_to_history(torrent, status: str):
        now = datetime.datetime.now().isoformat()
        added_iso = datetime.datetime.fromtimestamp(torrent.added_at).isoformat()
        
        finished_iso = now if status == "completed" else None
        removed_iso = now if status == "removed" else None
        
        task = SaveHistoryTask(
            db, torrent, status, finished_iso, removed_iso, added_iso)
        thread_pool.start(task)

    torrent_engine = TorrentEngine(
        default_save_path=os.path.expanduser("~/Downloads"),
        max_active=3, on_history=save_to_history
    )

    torrent_engine.load_active_state(db)

    def on_quit():
        torrent_engine.save_active_state(db)
        torrent_engine.shutdown()

    main_window = UI(torrent_engine, db)

    timer = QTimer()
    timer.timeout.connect(torrent_engine.update)
    timer.timeout.connect(main_window.refresh)
    timer.start(1000)

    save_timer = QTimer()
    save_timer.timeout.connect(lambda: torrent_engine.save_active_state(db))
    save_timer.start(300000)

    main_window.show()
    application.aboutToQuit.connect(on_quit)

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
