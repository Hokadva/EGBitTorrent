import os
import sqlite3


class TorrentModel:
    def __init__(self, db_path):
        self._db_path = db_path
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._connection = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS torrent_history (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                save_path TEXT NOT NULL,
                added_at TEXT NOT NULL,
                status TEXT NOT NULL,
                finished_at TEXT,
                removed_at TEXT,
                error_message TEXT
            )
        """)

    def add_history_record(
            self, torrent_id: str, name: str, size_bytes: int, save_path: str,
            added_at: str, status: str, finished_at: str = None,
            removed_at: str = None, error_message: str = None):
        with self._connection:
            self._connection.execute("""
                INSERT OR REPLACE INTO torrent_history
                (id, name, size_bytes, save_path, added_at, status,
                finished_at, removed_at, error_message) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (torrent_id, name, size_bytes, save_path, added_at,
                  status, finished_at, removed_at, error_message))

    def get_history(self):
        cursor = self._connection.execute("""
            SELECT id, name, size_bytes, save_path, added_at, status,
            finished_at, removed_at, error_message FROM torrent_history
            ORDER BY added_at DESC
        """)
        return cursor.fetchall()

    def clear_history(self):
        with self._connection:
            self._connection.execute("DELETE FROM torrent_history")

    def remove_elements(self, torrent_id: str):
        with self._connection:
            self._connection.execute("""
                DELETE FROM torrent_history [WHERE id = ?]
            """, (torrent_id, ))

    def close(self):
        self._connection.close()
