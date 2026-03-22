"""
NieR: Automata — Fishing Encyclopedia 100% Unlocker

Patches a NieR: Automata save file (SlotData_X.dat) to unlock all 41
entries in the Intel > Fishing Encyclopedia, bringing it to 100%.

Usage:
    python nier_fishing_encyclopedia_fix.py                  (auto-detect saves)
    python nier_fishing_encyclopedia_fix.py SlotData_0.dat   (specific file)

A backup (.bak) is always created before patching.
"""

import sys
import os
import shutil
import glob

# ---------------------------------------------------------------------------
# Save file layout
# ---------------------------------------------------------------------------
#
# The Fishing Encyclopedia completion is stored as a split bitfield that
# appears at two mirrored locations inside SlotData_X.dat:
#
#   PRIMARY                         MIRROR
#   0x3050C  [4 bytes] 32 species   0x385D8  [4 bytes]
#   0x30510  [2 bytes] padding      0x385DC  [2 bytes]
#   0x30512  [1 byte]  bit 7 → 1   0x385DE  [1 byte]  bit 7 (shared w/ other Intel)
#   0x30513  [1 byte]  8 species    0x385DF  [1 byte]
#                      ──────────                      ──────────
#                      41 total                        41 fishing + other Intel bits
#
# Setting every fishing bit to 1 marks all species as caught.
# Byte 0x385DE is OR-masked so that non-fishing Intel bits are preserved.
# ---------------------------------------------------------------------------

EXPECTED_FILE_SIZE = 235980

PATCHES = {
    # primary
    0x3050C: 0xFF,  0x3050D: 0xFF,  0x3050E: 0xFF,  0x3050F: 0xFF,
    0x30513: 0xFF,
    # mirror
    0x385D8: 0xFF,  0x385D9: 0xFF,  0x385DA: 0xFF,  0x385DB: 0xFF,
    0x385DF: 0xFF,
}

OR_PATCHES = {
    0x30512: 0x80,
    0x385DE: 0x80,
}

TOTAL_SPECIES = 41

DEFAULT_SAVE_DIR = os.path.join(
    os.path.expanduser("~"), "Documents", "My Games", "NieR_Automata"
)


def count_fish_bits(data: bytes) -> int:
    bits  = sum(bin(data[0x3050C + i]).count('1') for i in range(4))
    bits += bin(data[0x30512] & 0x80).count('1')
    bits += bin(data[0x30513]).count('1')
    return bits


def show_status(data: bytes) -> int:
    caught = count_fish_bits(data)
    pct = caught / TOTAL_SPECIES * 100
    bar_len = 30
    filled = int(bar_len * caught / TOTAL_SPECIES)
    bar = "#" * filled + "-" * (bar_len - filled)
    print(f"  [{bar}] {caught}/{TOTAL_SPECIES} ({pct:.0f}%)")
    return caught


def find_save_files() -> list[str]:
    if not os.path.isdir(DEFAULT_SAVE_DIR):
        return []
    return sorted(glob.glob(os.path.join(DEFAULT_SAVE_DIR, "SlotData_*.dat")))


def patch(path: str) -> bool:
    print(f"\n{'='*56}")
    print(f"  NieR: Automata - Fishing Encyclopedia Unlocker")
    print(f"{'='*56}\n")
    print(f"  File: {os.path.basename(path)}")
    print(f"  Path: {path}\n")

    if not os.path.isfile(path):
        print("  ERROR: file not found.")
        return False

    with open(path, 'rb') as f:
        data = bytearray(f.read())

    if len(data) != EXPECTED_FILE_SIZE:
        print(f"  WARNING: unexpected size ({len(data)} bytes, expected {EXPECTED_FILE_SIZE}).")
        try:
            resp = input("  Continue anyway? [y/N]: ").strip().lower()
        except EOFError:
            resp = 'n'
        if resp != 'y':
            print("  Aborted.")
            return False

    print("  Before:")
    caught = show_status(data)

    if caught >= TOTAL_SPECIES:
        print("\n  Already at 100% — nothing to do!")
        return True

    # Backup
    backup_path = path + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
        print(f"\n  Backup created: {os.path.basename(backup_path)}")
    else:
        print(f"\n  Backup exists:  {os.path.basename(backup_path)}")

    # Patch
    for off, val in PATCHES.items():
        data[off] = val
    for off, mask in OR_PATCHES.items():
        data[off] |= mask

    print("\n  After:")
    show_status(data)

    with open(path, 'wb') as f:
        f.write(data)

    print("\n  Done! Load your save in-game to verify.\n")
    return True


def main():
    if len(sys.argv) > 1:
        patch(sys.argv[1])
        return

    saves = find_save_files()

    if saves:
        print(f"\n  Save folder: {DEFAULT_SAVE_DIR}\n")
        for i, s in enumerate(saves):
            name = os.path.basename(s)
            slot_num = int(name.replace("SlotData_", "").replace(".dat", "")) + 1
            with open(s, 'rb') as f:
                d = f.read()
            caught = count_fish_bits(d)
            pct = caught / TOTAL_SPECIES * 100
            status = "100%" if caught >= TOTAL_SPECIES else f"{pct:.0f}%"
            print(f"  [{i + 1}] {name}  (Slot {slot_num})  — Encyclopedia: {status}")
        print(f"  [0] Enter a custom path\n")

        try:
            choice = input("  Select save to patch: ").strip()
            idx = int(choice)
        except (ValueError, EOFError):
            print("  Invalid input.")
            return

        if idx == 0:
            try:
                path = input("  Path to SlotData_X.dat: ").strip().strip('"')
            except EOFError:
                return
        elif 1 <= idx <= len(saves):
            path = saves[idx - 1]
        else:
            print("  Invalid selection.")
            return
    else:
        print(f"\n  No saves found in: {DEFAULT_SAVE_DIR}\n")
        try:
            path = input("  Path to SlotData_X.dat: ").strip().strip('"')
        except EOFError:
            return

    if not path:
        print("  No path given.")
        return

    patch(path)


if __name__ == "__main__":
    main()
