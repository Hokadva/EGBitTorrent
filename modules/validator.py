from dataclasses import dataclass
from typing import Optional
import libtorrent as lt
import os
import re


_MAGNET_RE = re.compile(
    r"^magnet:\?"
    r"(?=.*\bxt=urn:btih:[a-fA-F0-9]{40}\b)"
    r".*$",
    re.IGNORECASE,
)


@dataclass
class ValidationResult:
    ok: bool
    error: Optional[str] = None

def validate_magnet(url: str) -> ValidationResult:
    if not url or not url.strip():
        return ValidationResult(False, "Empty link")

    url = url.strip()

    if not url.startswith("magnet:"):
        return ValidationResult(False, "The link doesn't start with 'magnet:'")

    if not _MAGNET_RE.match(url):
        return ValidationResult(
            False, "Incorrect magnet url"
        )

    try:
        lt.parse_magnet_uri(url)
    except:
        return ValidationResult(False, f"libtorrent can't parse magnet url")

    return ValidationResult(True)

def validate_torrent_file(path: str) -> ValidationResult:
    if not path or not path.strip():
        return ValidationResult(False, "The file path isn't specified")

    path = path.strip().strip('"').strip('"')

    if not os.path.exists(path):
        return ValidationResult(False, "The file path isn't exists")

    if not os.path.isfile(path) or (
        (not path.endswith(".torrent")) and (not path.endswith(".TORRENT"))):
        return ValidationResult(False, "That object isn't torrent file")

    if not os.access(path, os.R_OK):
        return ValidationResult(False, "No rights to read the file")

    try:
        info = lt.torrent_info(path)

    except Exception as e:
        return ValidationResult(
            False, f"The file is corrupted or incorrect .torrent: {e}"
        )

    if not info.name():
        return ValidationResult(
            False, "The name is missing in the torrent file."
        )

    if info.num_files() == 0:
        return ValidationResult(
            False, "There are no files in the torrent file"
        )

    return ValidationResult(True)

def validate_save_path(path: str) -> ValidationResult:
    if not path or not path.strip():
        return ValidationResult(False, "The folder isn't specified")

    path = path.strip()

    if not os.path.exists(path):
        return ValidationResult(
            False, f"The folder isn't exists {path}"
        )

    if not os.path.isdir(path):
        return ValidationResult(False, f"That object isn't folder {path}")

    if not os.access(path, os.W_OK):
        return ValidationResult(False, "No rights to write in that folder")

    return ValidationResult(True)
