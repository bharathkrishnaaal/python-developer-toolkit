"""Find duplicate files by SHA-256 content hash; never deletes anything."""
from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(folder: Path) -> list[list[Path]]:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(folder)

    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in folder.rglob("*"):
        if path.is_file():
            try:
                by_size[path.stat().st_size].append(path)
            except OSError:
                continue

    groups: dict[str, list[Path]] = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for path in paths:
            try:
                groups[file_hash(path)].append(path)
            except OSError:
                continue
    return [sorted(paths) for paths in groups.values() if len(paths) > 1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    groups = find_duplicates(args.folder)
    if not groups:
        print("No duplicate files found.")
        return
    for index, group in enumerate(groups, 1):
        print(f"\nDuplicate group {index}:")
        for path in group:
            print(f"  {path}")
    print(f"\nFound {len(groups)} duplicate group(s). No files were changed.")


if __name__ == "__main__":
    main()
