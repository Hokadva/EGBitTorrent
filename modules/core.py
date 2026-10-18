import os
import shutil
from typing import Optional
import re
from enum import Enum
from urllib.parse import parse_qs, unquote

POSTFS = ("B", "KB", "MB", "GB", "TB")
NUMS = "0123456789."


class Colors(str, Enum):
    red = "#FF0000"
    error_red = "#EF4444"
    orange = "#FFA500"
    green = "#00FF00"
    succes_green = "#22C55E"


def colorize(text: str, color: Colors) -> str:
    return f"<span style='color:{color}'>{text}</span>"

def folder_remove(path: str) -> str:
    try:
        os.rmdir(path)
    except Exception:
        pass

    return path

def new_root_if_necessary(
        paths, folder_path: str, torrent_name: str,
        is_necessary: bool) -> str:
    if not is_necessary:
        return (folder_path, False)

    new_path = smart_folder_name_getter(
        os.path.join(folder_path, torrent_name))

    return (new_path, True)

def smart_folder_name_getter(path: str) -> str:
    if not os.path.exists(path):
        return path

    numx = 1
    
    while os.path.exists(path + f" ({numx})"):
        numx += 1

    return path + f" ({numx})"

def smart_folder_creating(path) -> str:
    path = smart_folder_name_getter(
        path
    )
    os.makedirs(path)

    return path

def find_common_root(paths) -> Optional[str]:
    """
    Возвращает общий корневой путь для всех файлов, если он есть.
    Например, ["a/b/c.mkv", "a/b/d.mkv"] → "a/b"
            ["a/x.mkv", "b/y.mkv"] -> None
            ["file.mkv"] -> None (один файл — нет корня)
    """
    if len(paths) <= 1:
        return None

    split_paths = [p.split("/") for p in paths]

    common = []

    for i, part in enumerate(split_paths[0][:-1]):
        if all(len(p) > i + 1 and p[i] == part for p in split_paths):
            common.append(part)
        else:
            break

    return "/".join(common) if common else None

def approximate_byte_size(size: str) -> float:
    size = size.upper()
    answer = 0
    for deegre, postf in enumerate(POSTFS):
        if postf in size:
            answer = float("".join(tuple(
                nm if nm in NUMS else "" for nm in size)
            )) * 1024 ** (deegre)

            if postf != POSTFS[0]:
                break

    return answer

def approximate_byte_speed(size: str) -> float:
    return approximate_byte_size(size[:-2])

def human_size(size: int) -> str:
    if size is None:
        return "-"

    for tp in POSTFS:
        if size < 1024:
            return f"{size} {tp}"

        size = round(size / 1024, 2)

    return f"{size} {tp}"

def human_rate(speed: int):
    if not speed:
        return "0 B/s"

    return f"{human_size(speed)}/s"

def human_time(seconds: float) -> str:
    if seconds <= 0 or seconds > 30 * 60 * 60 * 24:
        return "-"

    seconds = round(seconds)
    hours = seconds // 60 // 60
    minutes = seconds // 60 - hours * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60

    if hours:
        return f"{hours} h {minutes} m"
    if minutes:
        return f"{minutes} m {seconds} s"

    return f"{seconds} s"

def get_free_disk_space(path: str) -> int:
    """Свободное место на диске в байтах. 0 — если путь недоступен."""
    try:
        usage = os.statvfs(path) if hasattr(os, "statvfs") else None
        if usage:
            return usage.f_bavail * usage.f_frsize

    except Exception:
        pass

    try:
        return shutil.disk_usage(path).free

    except Exception:
        return 0

def extract_magnet_name(magnet: str) -> str:
    try:
        query = magnet.split("?", 1)[1]
        params = parse_qs(query)
        dn = params.get("dn", [""])[0]
        if dn:
            name = unquote(dn).strip()
            return clear_filename(name)

    except Exception:
        pass

    match = re.search(r"urn:btih:([a-fA-F0-9]{40})", magnet)
    if match:
        return f"Torrent_{match.group(1)[:12].lower()}"

    return "New_torrent"

def clear_filename(name: str) -> str:
    """Убирает символы, запрещённые в именах файлов Windows."""
    forbidden = '<>:"/\\|?*'
    for ch in forbidden:
        name = name.replace(ch, "_")

    name = name.rstrip(" .")
    return name[:120] or "Torrent"
