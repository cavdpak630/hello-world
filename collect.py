#!/usr/bin/env python3
"""
Thesis Pilot Study — Data Collection Script

Run after each session:
  python collect.py
"""

import shutil
import sys
from datetime import date
from pathlib import Path

# ── CONFIGURE ONCE ────────────────────────────────────────────────

# Root of your XR pipeline project (where data\ and unity\ live)
BASE = Path(r"D:\Studies\Thesis\Project Codes\Foot_XR_Pipeline")

# The 3 files collected per participant (relative to BASE)
PARTICIPANT_FILES = [
    r"data\live\session_R_562.csv",
    r"data\live\session_L_561.csv",
    r"unity\StepSight_Pilot_Test\detected_gestures.csv",
]

# Where per-participant folders are created
OUTPUT_ROOT = Path(r"D:\Studies\Thesis\Pilot_Study_Docs\Pilot_Study_Outputs")

# Unity P4_Data: copied entirely into UnityOutputs after every session
P4_DATA_SRC  = BASE / r"unity\StepSight_Pilot_Test\P4_Data"
P4_DATA_DEST = OUTPUT_ROOT / "UnityOutputs"

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
    print()
    print("=" * 60)
    print("   Thesis Pilot Study  —  Data Collection")
    print("=" * 60)

    pid = _validate_id(input("\n  Participant ID: "))

    folder_name = f"{pid}_{date.today().strftime('%Y%m%d')}"
    output_dir = OUTPUT_ROOT / folder_name

    if output_dir.exists():
        _die(
            f"Output folder already exists:\n  {output_dir}\n\n"
            "  The participant may already have been collected today.\n"
            "  Rename or remove the existing folder if you need to re-collect."
        )

    output_dir.mkdir(parents=True)

    print(f"\n  Output  →  {output_dir}\n")

    # ── Participant files ──────────────────────────────────────────
    print("  Participant files:")
    print("  " + "-" * 56)

    copied = 0
    missing = 0

    for rel in PARTICIPANT_FILES:
        src = BASE / rel
        dest_name = f"{pid}_{src.name}"
        dest = output_dir / dest_name

        if src.exists():
            shutil.copy2(src, dest)
            print(f"  OK      {src.name}")
            print(f"          → {dest_name}")
            copied += 1
        else:
            print(f"  MISSING {src}")
            missing += 1

    print("  " + "-" * 56)
    print(f"  {copied} file(s) copied, {missing} missing.")

    # ── Unity P4_Data ─────────────────────────────────────────────
    print("\n  Unity P4_Data → UnityOutputs:")
    print("  " + "-" * 56)

    if not P4_DATA_SRC.exists():
        print(f"  MISSING {P4_DATA_SRC}")
        missing += 1
    else:
        shutil.copytree(P4_DATA_SRC, P4_DATA_DEST, dirs_exist_ok=True)
        print(f"  OK      {P4_DATA_SRC.name}  →  {P4_DATA_DEST}")

    print("  " + "-" * 56)

    # ── Summary ───────────────────────────────────────────────────
    if missing:
        print(f"\n  Done (with {missing} missing file(s)). Check paths at the top of collect.py.\n")
        sys.exit(1)
    else:
        print(f"\n  All done!  Folder: {folder_name}\n")


if __name__ == "__main__":
    main()
