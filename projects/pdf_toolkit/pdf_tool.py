"""Merge, split, or extract text from PDF files using pypdf."""
from __future__ import annotations

import argparse
from pathlib import Path


def get_reader(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("Install dependencies with: python -m pip install -r requirements.txt") from exc
    if not path.is_file():
        raise FileNotFoundError(path)
    return PdfReader(str(path))


def merge(inputs: list[Path], output: Path) -> None:
    from pypdf import PdfWriter
    writer = PdfWriter()
    for path in inputs:
        reader = get_reader(path)
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        writer.write(stream)


def split(source: Path, output_dir: Path) -> None:
    from pypdf import PdfWriter
    reader = get_reader(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        output = output_dir / f"{source.stem}_page_{index}.pdf"
        with output.open("wb") as stream:
            writer.write(stream)


def extract(source: Path) -> None:
    reader = get_reader(source)
    for index, page in enumerate(reader.pages, 1):
        print(f"\n--- Page {index} ---\n")
        print(page.extract_text() or "[No extractable text on this page]")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    merge_parser = sub.add_parser("merge")
    merge_parser.add_argument("output", type=Path)
    merge_parser.add_argument("inputs", nargs="+", type=Path)
    split_parser = sub.add_parser("split")
    split_parser.add_argument("input", type=Path)
    split_parser.add_argument("output_dir", type=Path)
    extract_parser = sub.add_parser("extract")
    extract_parser.add_argument("input", type=Path)
    args = parser.parse_args()

    if args.command == "merge":
        merge(args.inputs, args.output)
        print(f"Merged {len(args.inputs)} file(s) into {args.output}")
    elif args.command == "split":
        split(args.input, args.output_dir)
        print(f"Split {args.input} into {args.output_dir}")
    else:
        extract(args.input)


if __name__ == "__main__":
    main()
