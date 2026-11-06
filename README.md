# Python Developer Toolkit

A collection of small, practical Python command-line tools for everyday development tasks.

This repository is organized as independent projects. Each tool has a focused purpose, uses the Python standard library wherever practical, and includes usage instructions and tests.

## Projects

| Project | Description |
|---|---|
| Smart File Organizer | Sort files into folders by extension, with a dry-run mode |
| PDF Toolkit | Merge, split, and extract text from PDFs using `pypdf` |
| System Monitor | Display CPU, memory, disk, and network statistics |
| Duplicate File Finder | Find duplicate files by content hash |
| Automation Toolkit | Batch rename files safely using a preview-first workflow |

## Requirements

- Python 3.10 or newer
- Install optional dependencies for the PDF and system-monitor tools:

```bash
python -m pip install -r requirements.txt
```

## Quick start

Run any tool from the repository root:

```bash
python projects/file_organizer/organize.py ./Downloads --dry-run
python projects/duplicate_finder/find_duplicates.py ./Documents
python projects/system_monitor/monitor.py
python projects/automation/batch_rename.py ./photos --prefix holiday --dry-run
```

PDF commands:

```bash
python projects/pdf_toolkit/pdf_tool.py merge output.pdf a.pdf b.pdf
python projects/pdf_toolkit/pdf_tool.py split input.pdf ./pages
python projects/pdf_toolkit/pdf_tool.py extract input.pdf
```

## Testing

```bash
python -m unittest discover -s tests -v
```

## Project principles

- Preview destructive or bulk operations before applying them.
- Never delete or overwrite user data silently.
- Keep dependencies small and documented.
- Prefer clear, maintainable code over clever shortcuts.

## Repository structure

```text
.
├── projects/
│   ├── automation/
│   ├── duplicate_finder/
│   ├── file_organizer/
│   ├── pdf_toolkit/
│   └── system_monitor/
├── tests/
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## Attribution and scope

This toolkit is intended to be an independently maintained collection of practical utilities. Add your own improvements, tests, examples, and documentation as you work on it. Do not copy code from other projects without preserving the applicable license and attribution.

## Roadmap

- Add cross-platform integration tests.
- Add structured logging and configuration files.
- Publish versioned releases with changelogs.
- Accept documented bug reports and feature requests.
