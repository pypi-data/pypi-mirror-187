from pathlib import Path

from printbuddies import clear, print_in_place


def crawl(start_dir: Path | str, quiet: bool = False) -> list[Path]:
    """Recursively crawl a directory tree
    and return a list of files as pathlib.Path objects.
    :param quiet: If True, don't print information about the crawl."""
    files = []
    for path in Path(start_dir).iterdir():
        if not quiet:
            print_in_place(f"Crawling {path}")
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(crawl(path))
    if not quiet:
        clear()
    return files


def get_directory_size(start_dir: Path | str) -> int:
    """Return the size of a directory tree in bytes."""
    return sum(file.stat().st_size for file in crawl(start_dir, quiet=True))


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
