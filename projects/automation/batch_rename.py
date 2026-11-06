"""Preview or apply a safe, sequential batch rename."""
from __future__ import annotations

import argparse
from pathlib import Path


def build_plan(folder: Path, prefix: str, start: int = 1) -> list[tuple[Path, Path]]:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    if start < 0:
        raise ValueError("start must be non-negative")

    items = sorted(path for path in folder.iterdir() if path.is_file())
    plan = []
    for number, source in enumerate(items, start):
        target = source.with_name(f"{prefix}_{number:03d}{source.suffix.lower()}")
        if target != source and target.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
        plan.append((source, target))
    return plan


def apply_plan(plan: list[tuple[Path, Path]]) -> None:
    # Stage names first to avoid collisions when one target equals another source.
    staged = []
    for index, (source, target) in enumerate(plan):
        temporary = source.with_name(f".rename_tmp_{index}_{source.name}")
        if temporary.exists():
            raise FileExistsError(temporary)
        source.rename(temporary)
        staged.append((temporary, target))
    for temporary, target in staged:
        if target.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
        temporary.rename(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--apply", action="store_true",
                        help="apply the rename (default is preview only)")
    args = parser.parse_args()
    plan = build_plan(args.folder, args.prefix, args.start)
    for source, target in plan:
        print(f"{source.name} -> {target.name}")
    if args.apply:
        apply_plan(plan)
        print(f"Renamed {len(plan)} file(s).")
    else:
        print(f"Preview only: {len(plan)} file(s). Use --apply to rename.")


if __name__ == "__main__":
    main()
