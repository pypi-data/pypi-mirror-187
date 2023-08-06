from pathlib import Path
from typing import Generator


def crawl(start_dir: Path | str) -> Generator[Path, None, None]:
    """Glorified rglob.
    Returns a generator yielding all files in start_dir and
    its sub directories."""
    return Path(start_dir).rglob("*.*")


def get_directory_size(start_dir: Path | str) -> int:
    """Return the size of a directory tree in bytes."""
    return sum(file.stat().st_size for file in crawl(start_dir))


def format_size(size_bytes: int) -> str:
    """Return a string with appropriate unit suffix
    and rounded to two decimal places.
    i.e. format_size(1572166) returns "1.57 mb" """
    if size_bytes < 1000:
        return f"{round(size_bytes, 2)} bytes"
    for unit in ["kb", "mb", "gb", "tb"]:
        size_bytes /= 1000
        if size_bytes < 1000:
            return f"{round(size_bytes, 2)} {unit}"
