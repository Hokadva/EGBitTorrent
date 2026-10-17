from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time
from modules.core import human_rate, human_size, human_time


class TorrentState(Enum):
    """Состояние торрента — маппится из libtorrent, но не зависит от него."""
    QUEUED = "QUEUED"
    CHECKING = "CHECKING"
    METADATA = "METADATA"
    DOWNLOADING = "DOWNLOADING"
    SEEDING = "SEEDING"
    FINISHED = "FINISHED"
    PAUSED = "PAUSED"
    ERROR = "ERROR"


class DuplicateTorrentError(Exception):
    def __init__(self, torrent_id: str):
        self.torrent_id = torrent_id
        super().__init__(f"Torrent already exists: {torrent_id}")


@dataclass
class TorrentFileInfo:
    """Информация об одном файле внутри торрента (для вкладки «Файлы»)."""
    index: int
    path: str
    byte_size: int
    progress: float
    priority: int

@dataclass
class TorrentFile:
    id: str
    name: str
    files_count: int = 0
    byte_size: int = 0
    progress: float = 0.0
    state: TorrentState = TorrentState.QUEUED
    seeds: int = 0
    seeds_total: int = 0
    peers: int = 0
    peers_total: int = 0
    downloading_rate: int = 0
    upload_rate: int = 0
    downloading_bytes: int = 0
    upload_bytes: int = 0
    save_path: str = 0
    added_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None
    error_message: Optional[str] = None
    groups: set = field(default_factory=set)

    @property
    def size_human(self) -> str:
        return human_size(self.byte_size)

    @property
    def downloaded_human(self) -> str:
        return human_size(self.downloading_bytes)

    @property
    def uploaded_human(self) -> str:
        return human_size(self.upload_bytes)

    @property
    def downloaded_rate_human(self) -> str:
        return human_rate(self.downloading_rate)

    @property
    def uploaded_rate_human(self) -> str:
        return human_rate(self.upload_rate)

    @property
    def eta_human(self) -> str:
        if self.downloading_rate <= 0 or self.progress >= 1.0:
            return "—"
        remaining = self.byte_size * (1.0 - self.progress)
        return human_time(remaining / self.download_rate)

    @property
    def is_active(self) -> bool:
        return self.state in (TorrentState.DOWNLOADING,
                              TorrentState.SEEDING,
                              TorrentState.CHECKING,
                              TorrentState.METADATA)
