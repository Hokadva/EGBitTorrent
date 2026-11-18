import os
import sqlite3


class TorrentModel:
    def __init__(self, db_path):
        self._db_path = db_path
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._connection = sqlite3.connect(db_path)
        self._connection.execute("PRAGMA foreign_keys = ON")
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
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS active_torrents (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                source BLOB NOT NULL,
                save_path TEXT NOT NULL,
                paused INTEGER NOT NULL DEFAULT 0
            )
        """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS traffic (
                id TEXT PRIMARY KEY,
                downloaded INTEGER NOT NULL DEFAULT 0,
                uploaded INTEGER NOT NULL DEFAULT 0
            )
        """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL UNIQUE
            )
        """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS torrent_groups (
                group_id INTEGER NOT NULL,
                torrent_id TEXT NOT NULL,
                PRIMARY KEY (group_id, torrent_id),
                FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
                FOREIGN KEY (torrent_id) REFERENCES active_torrents(id) ON DELETE CASCADE
            )
        """)
        self._connection.commit()

    def get_traffic(self, torrent_id) -> tuple[int, int]:
        row = self._connection.execute(
            "SELECT downloaded, uploaded FROM traffic WHERE id=?",
            (torrent_id,)).fetchone()
        return row or (0, 0)

    def _get_group_id(self, group_name: str) -> int:
        return self._connection.execute("""
            SELECT id FROM groups WHERE text = ?
        """, (group_name, )).fetchone()[0]

    def get_group(self, group_name: str) -> list:
        group_id = self._get_group_id(group_name)
        return [row[0] for row in self._connection.execute("""
            SELECT torrent_id FROM torrent_groups WHERE group_id=?
        """, (group_id, )).fetchall()]

    def create_group(self, group_name: str):
        self._connection.execute(
            "INSERT OR IGNORE INTO groups (text) VALUES (?)",
            (group_name,),
        )
        self._connection.commit()

    def remove_group(self, group_name: str):
        self._connection.execute(
            "DELETE FROM groups WHERE text = ?", (group_name, )
        )
        self._connection.commit()

    def get_groups(self):
        return [row[0] for row in self._connection.execute("""
            SELECT text FROM groups
        """).fetchall()]

    def remove_link(self, group_name: str, torrent_id: str):
        group_id = self._get_group_id(group_name)
        self._connection.execute("""
            DELETE FROM torrent_groups WHERE (group_id = ? AND
            torrent_id = ?)
        """, (group_id, torrent_id))
        self._connection.commit()

    def create_link(self, group_name: str, torrent_id: str) -> bool:
        group_id = self._get_group_id(group_name)
        if group_id is None:
            return False
        cur = self._connection.execute(
            """INSERT OR IGNORE INTO
            torrent_groups(group_id, torrent_id) VALUES (?, ?)""",
            (group_id, torrent_id),
        )
        self._connection.commit()
        return cur.rowcount > 0

    def set_traffic(self, torrent_id, downloaded, uploaded):
        with self._connection:
            self._connection.execute(
                "INSERT OR REPLACE INTO traffic VALUES (?,?,?)",
                (torrent_id, int(downloaded), int(uploaded)))

    def total_traffic(self) -> tuple[int, int]:
        row = self._connection.execute(
            "SELECT COALESCE(SUM(downloaded),0), COALESCE(SUM(uploaded),0) "
            "FROM traffic").fetchone()
        return row[0], row[1]

    def save_active(self, torrent_id, kind, source, save_path, paused):
        with self._connection:
            self._connection.execute(
                "INSERT OR REPLACE INTO active_torrents VALUES (?,?,?,?,?)",
                (torrent_id, kind, source, save_path, int(paused)))

    def set_active_paused(self, torrent_id: str, paused: bool):
        with self._connection:
            self._connection.execute(
                "UPDATE active_torrents SET paused=? WHERE id=?",
                (int(paused), torrent_id))

    def remove_active(self, torrent_id: str):
        with self._connection:
            self._connection.execute(
                "DELETE FROM active_torrents WHERE id=?", (torrent_id,))

    def get_active(self):
        return self._connection.execute(
            "SELECT id, kind, source, save_path, paused "
            "FROM active_torrents").fetchall()

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
                DELETE FROM torrent_history WHERE id = ?
            """, (torrent_id, ))

    @property
    def total_remove(self) -> int:
        cursor = self._connection.execute("""
            SELECT COUNT(*) FROM torrent_history
            WHERE status='removed'
        """)
        return cursor.fetchall()[0][0]

    @property
    def total_records(self) -> int:
        cursor = self._connection.execute("SELECT COUNT(*) FROM torrent_history")
        return cursor.fetchall()[0][0]

    def close(self):
        self._connection.close()
