"""Organize files into folders based on their extensions."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def category_for(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if not suffix:
        return "no_extension"
    categories = {
        "images": {"png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"},
        "documents": {"pdf", "doc", "docx", "txt", "rtf", "odt"},
        "spreadsheets": {"csv", "xls", "xlsx", "ods"},
        "audio": {"mp3", "wav", "flac", "aac", "ogg"},
        "video": {"mp4", "mkv", "mov", "avi", "webm"},
        "archives": {"zip", "rar", "7z", "tar", "gz"},
        "code": {"py", "js", "ts", "java", "c", "cpp", "html", "css"},
    }
    for name, extensions in categories.items():
        if suffix in extensions:
            return name
    return "others"


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = True) -> list[tuple[Path, Path]]:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(folder)

    planned = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        target_dir = folder / category_for(item)
        target = unique_destination(target_dir / item.name)
        planned.append((item, target))
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(target))
    return planned


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--apply", action="store_true",
                        help="perform moves (default is preview only)")
    args = parser.parse_args()
    moves = organize(args.folder, dry_run=not args.apply)
    for source, target in moves:
        print(f"{source.name} -> {target.parent.name}/{target.name}")
    print(f"{'Planned' if not args.apply else 'Moved'} {len(moves)} file(s).")


if __name__ == "__main__":
    main()
