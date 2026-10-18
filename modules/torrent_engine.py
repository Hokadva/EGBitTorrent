import libtorrent as lt
import sys
import os
import threading
from typing import Dict, List, Optional
import time

from modules.torrent import (
    TorrentFile, DuplicateTorrentError, TorrentFileInfo, TorrentState)
from modules.core import extract_magnet_name, find_common_root


class TorrentEngine:
    _STATE_MAP = {
        lt.torrent_status.queued_for_checking: TorrentState.CHECKING,
        lt.torrent_status.checking_files: TorrentState.CHECKING,
        lt.torrent_status.downloading_metadata: TorrentState.METADATA,
        lt.torrent_status.downloading: TorrentState.DOWNLOADING,
        lt.torrent_status.finished: TorrentState.SEEDING,
        lt.torrent_status.seeding: TorrentState.SEEDING,
        lt.torrent_status.allocating: TorrentState.CHECKING,
        lt.torrent_status.checking_resume_data: TorrentState.CHECKING,
    }

    def __init__(self, default_save_path: str, max_active: int = 3):
        """Инициализация класса"""
        self._default_savepath = default_save_path
        self.max_active = max_active

        self._lock = threading.RLock()
        self._session: Optional[lt.session] = None
        self._handles: Dict[str, lt.torrent_handle] = {}
        self._torrents: Dict[str, TorrentFile] = {}
        self._queued: List[str] = []

        self._init_session()

    @property
    def default_savepath(self):
        return self._default_savepath

    @default_savepath.setter
    def default_savepath(self, dfsp):
        self._default_savepath = dfsp

    def _init_session(self):
        """Инициализация торрент-сессии — безопасный вариант"""
        self._session = lt.session()
        self._session.listen_on(6881, 6891)

        try:
            self._session.apply_settings({
                "user_agent": "EGBitTorrent/1.0",
                "download_rate_limit": 0,
                "upload_rate_limit": 0,
            })
        except Exception as e:
            print(f"apply_settings failed: {e}")

    def _register(
            self, torrent_id: str, handle, name: str,
            save_path: str, start_now: bool):
        """Добавляет торрент в очередь или загрузку"""
        with self._lock:
            self._handles[torrent_id] = handle

            model = TorrentFile(
                id=torrent_id,
                name=name,
                save_path=save_path,
                state=TorrentState.QUEUED if start_now else TorrentState.PAUSED,
            )
            self._torrents[torrent_id] = model

            if not start_now:
                handle.pause()
                return

            self._queued.append(torrent_id)
            self._start_next()

    def add_magnet(self, url: str, save_path = None, start_now: bool = True):
        """Добавляет торрент по magnet ссылке"""
        save_path = save_path or self._default_savepath

        params = lt.parse_magnet_uri(url)
        params.save_path = save_path

        torrent_id = str(params.info_hashes.v1)
        self._duplicate_check(torrent_id)

        with self._lock:
            handle = self._session.add_torrent(params)

        self._register(
            torrent_id, handle, extract_magnet_name(url), save_path, start_now)

        return torrent_id

    def get_handle(self, torrent_id: str):
        with self._lock:
            return self._handles.get(torrent_id)

    def _duplicate_check(self, torrent_id: str):
        if torrent_id in self._torrents:
            raise DuplicateTorrentError(torrent_id)

    def add_torrent_file(self, path, save_path = None, start_now: bool = True):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found {path}")

        save_path = save_path or self._default_savepath
        info = lt.torrent_info(path)

        torrent_id = str(info.info_hashes().v1)
        self._duplicate_check(torrent_id)

        params = lt.add_torrent_params()
        params.ti = info
        params.save_path = save_path

        with self._lock:
            handle = self._session.add_torrent(params)

        self._register(torrent_id, handle, name=info.name(),
                    save_path=save_path, start_now=start_now)
        return torrent_id

    def _active_count(self) -> int:
        """Считает чисо активных загрузок"""
        return sum(1 for t in self._torrents.values() if t.is_active)

    def _start_next(self):
        """Запускает следующий торрент на загрузку"""
        while self._queued and self._active_count() < self.max_active:
            torrent_id = self._queued.pop(0)
            handle = self._handles.get(torrent_id)
            if handle is None:
                continue

            handle.resume()
            self._torrents[torrent_id].state = TorrentState.DOWNLOADING

    def _on_torrent_finished(self, torrent_id: str):
        """Завершает процедуру загрузки"""
        with self._lock:
            torrent = self._torrents.get(torrent_id)
            if torrent:
                torrent.state = TorrentState.SEEDING
                torrent.finished_at = time.time()
            self._start_next()

    def pause(self, torrent_id: str):
        """Останавливает торрент загрузку"""
        with self._lock:
            handle = self._handles.get(torrent_id)
            if handle:
                handle.pause()
            torrent = self._torrents.get(torrent_id)
            if torrent:
                torrent.state = TorrentState.PAUSED
                if torrent_id in self._queued:
                    self._queued.remove(torrent_id)

    def resume(self, torrent_id: str):
        """Возобновляет торрент — ставит в очередь, _start_next решает."""
        with self._lock:
            if torrent_id in self._queued:
                return

            torrent = self._torrents.get(torrent_id)
            if torrent is None or torrent.state == TorrentState.DOWNLOADING:
                return

            self._queued.append(torrent_id)
            torrent.state = TorrentState.QUEUED
            self._start_next()

    def remove(self, torrent_id: str, delete_files: bool = False):
        """Удаляет торрент. Работает даже при невалидном handle."""
        with self._lock:
            handle = self._handles.get(torrent_id)

            if handle is not None:
                try:
                    if handle.is_valid():
                        try:
                            handle.pause()
                        except Exception:
                            pass

                        flags = lt.options_t.delete_files if delete_files else 0
                        self._session.remove_torrent(handle, flags)
                except Exception as e:
                    print(f"[remove] error: {e}")

            self._handles.pop(torrent_id, None)
            self._torrents.pop(torrent_id, None)
            self._queued = [tid for tid in self._queued if tid != torrent_id]

            self._start_next()

    def move_torrent(self, source_id: str, target_id: str):
        with self._lock:
            if not(source_id in self._torrents and target_id in self._torrents):
                return

            items = list(self._torrents.items())
            source_idx = next(
                nm for nm, (idx, it) in enumerate(items) if idx == source_id)
            target_idx = next(
                nm for nm, (idx, it) in enumerate(items) if idx == target_id)

            item = items.pop(source_idx)
            if source_idx < target_idx:
                target_idx -= 1
            items.insert(target_idx, item)
            self._torrents = dict(items)

    def update(self):
        with self._lock:
            for torrent_id, handle in list(self._handles.items()):
                torrent = self._torrents.get(torrent_id)
                if torrent is None:
                    continue

                if not handle.is_valid():
                    torrent.state = TorrentState.ERROR
                    torrent.error_message = "Handle invalid"
                    continue

                try:
                    status = handle.status()

                except Exception as e:
                    torrent.state = TorrentState.ERROR
                    torrent.error_message = f"Error {e}"
                    continue

                if status.errc and status.errc.value() != 0:
                    torrent.state = TorrentState.ERROR
                    torrent.error_message = status.errc.message()
                    try:
                        handle.pause()
                    except:
                        pass
                    continue

                torrent.progress = float(status.progress)
                torrent.seeds = status.num_seeds
                torrent.seeds_total = status.num_complete
                torrent.peers = status.num_peers
                torrent.peers_total = status.num_incomplete
                torrent.downloading_rate = status.download_rate
                torrent.upload_rate = status.upload_rate
                torrent.downloading_bytes = status.total_done
                torrent.upload_bytes = status.total_upload

                if status.paused:
                    torrent.state = TorrentState.PAUSED
                elif not status.has_metadata:
                    torrent.state = TorrentState.METADATA
                else:
                    torrent.state = self._STATE_MAP.get(status.state, TorrentState.QUEUED)

                if status.has_metadata and handle.torrent_file():
                    tf = handle.torrent_file()
                    if torrent.name.startswith("magnet:"):
                        torrent.name = tf.name()
                    if torrent.byte_size == 0:
                        torrent.byte_size = tf.total_size()
                    if torrent.files_count == 0:
                        torrent.files_count = tf.num_files()

                if torrent.progress >= 1.0:
                    torrent.downloading_rate = 0
                    if torrent.finished_at is None:
                        self._on_torrent_finished(torrent_id)

    def get_all_torrents(self) -> List[TorrentFile]:
        with self._lock:
            return list(self._torrents.values())

    def get(self, torrent_id: str) -> Optional[TorrentFile]:
        with self._lock:
            return self._torrents.get(torrent_id)

    def get_files(self, torrent_id: str) -> List[TorrentFileInfo]:
        with self._lock:
            handle = self._handles.get(torrent_id)
            if handle is None or not handle.is_valid():
                return []

            if not handle.status().has_metadata:
                return []

            torrent_file = handle.torrent_file()
            if torrent_file is None:
                return []

            storage = torrent_file.files()
            priorities = handle.file_priorities()
            result = []

            for idx in range(storage.num_files()):
                result.append(
                    TorrentFileInfo(
                        index=idx,
                        path=storage.file_path(idx),
                        size_bytes=storage.file_size(idx),
                        progress=handle.file_progress([idx])[0] / max(storage.file_size(idx), 1),
                        priority=priorities[idx] if idx < len(priorities) else 4
                    )
                )

            return result

    def _dht_nodes(self) -> int:
        try:
            return self._session.status().dht_nodes
        except:
            return 0

    def set_max_active(self, num: int):
        with self._lock:
            self.max_active = max(int(num), 1)
            self._start_next()

    def set_download_limit(self, bytes_per_sec: int):
        self._session.apply_settings({"download_rate_limit": int(bytes_per_sec)})

    def set_upload_limit(self, bytes_per_sec: int):
        self._session.apply_settings({"upload_rate_limit": int(bytes_per_sec)})

    def shutdown(self):
        with self._lock:
            try:
                self._session.pause()
            except Exception:
                pass
            self._handles.clear()
            self._torrents.clear()
            self._queued.clear()
