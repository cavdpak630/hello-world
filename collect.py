#!/usr/bin/env python3
"""
Thesis Pilot Study — Data Collection Script

Run after each session to package a participant's files:
  python collect.py

To overwrite an already-existing participant folder:
  python collect.py --overwrite
"""

import shutil
import sys
from pathlib import Path

# ── CONFIGURE ONCE ────────────────────────────────────────────────
# List each source folder and the exact filenames to collect from it.
# A folder can have more than one file — just add more entries to its "files" list.

SOURCE_FOLDERS = [
    {
        "path": r"C:\path\to\folder1",       # ← replace with your actual folder path
        "files": ["filename1.csv"],           # ← replace with your actual filename(s)
    },
    {
        "path": r"C:\path\to\folder2",       # ← replace with your actual folder path
        "files": ["filename2.log"],           # ← replace with your actual filename(s)
    },
    {
        "path": r"C:\path\to\folder3",       # ← replace with your actual folder path
        "files": ["filename3.json"],          # ← replace with your actual filename(s)
    },
]

# Root folder where per-participant sub-folders will be created.
OUTPUT_ROOT = r"C:\path\to\participants"     # ← replace with your actual output path

# ──────────────────────────────────────────────────────────────────


_INVALID_CHARS = set('/\\:*?"<>|')


def _validate_id(pid: str) -> str:
    pid = pid.strip()
    if not pid:
        _die("Participant ID cannot be empty.")
    bad = [c for c in pid if c in _INVALID_CHARS]
    if bad:
        _die(f"Participant ID contains invalid character(s): {' '.join(repr(c) for c in bad)}")
    return pid


def _die(message: str) -> None:
    print(f"\nERROR: {message}")
    sys.exit(1)


def main() -> None:
    overwrite = "--overwrite" in sys.argv

    print()
    print("=" * 60)
    print("   Thesis Pilot Study  —  Data Collection")
    print("=" * 60)

    pid = _validate_id(input("\n  Participant ID: "))

    output_dir = Path(OUTPUT_ROOT) / pid

    if output_dir.exists() and not overwrite:
        _die(
            f"Folder already exists:\n  {output_dir}\n\n"
            "  Re-run with --overwrite to replace its contents."
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  Output  →  {output_dir}\n")
    print(f"  {'STATUS':<7} {'SOURCE FILE'}")
    print("  " + "-" * 70)

    copied = 0
    missing = 0

    for entry in SOURCE_FOLDERS:
        folder = Path(entry["path"])
        for filename in entry["files"]:
            src = folder / filename
            dest_name = f"{pid}_{filename}"
            dest = output_dir / dest_name

            if src.exists():
                shutil.copy2(src, dest)
                print(f"  OK      {src}")
                print(f"          → {dest_name}")
                copied += 1
            else:
                print(f"  MISSING {src}")
                print(f"          (skipped)")
                missing += 1

    print("  " + "-" * 70)
    print(f"\n  {copied} file(s) copied, {missing} missing.\n")

    if missing:
        print("  Check the SOURCE_FOLDERS paths and filenames at the top of collect.py.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
