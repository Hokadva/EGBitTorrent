import os
import shutil


POSTFS = ("B", "KB", "MB", "GB", "TB")
NUMS = "0123456789."


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