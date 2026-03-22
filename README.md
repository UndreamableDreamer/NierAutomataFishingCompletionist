# NieR: Automata — Fishing Encyclopedia Unlocker

A simple Python script that patches your NieR: Automata save file to unlock all **41 entries** in the **Intel > Fishing Encyclopedia**, bringing it to 100% completion.

Fishing in NieR: Automata is entirely RNG-based and some fish are extremely rare and can take hours of real time to catch.
I wasted 10 hours of my time fishing and 4 hours researching, using Claude Opus 4.6 (yes, that was made with help of AI, bite me) to write this script so you can live your life.

Idea of taking 100% completed save wasn't on the table for me, because I want to get other things myself, so...
This tool lets you skip the grind while keeping the rest of your save intact. Will work on any percentage of your savefile (hopefully) and also will produce a backup so you can rollback if something gets wrong. 

## Requirements

- Python 3.6+

## Usage

### Automatic (recommended)

Place the script anywhere and run it — it will find your saves automatically:

```
py nier_fishing_encyclopedia.py
```

The script detects saves in the default Steam location:
```
Documents\My Games\NieR_Automata\
```

It shows each slot's current encyclopedia completion and lets you pick which one to patch.

### Manual

Pass the path to a specific save file:

```
py nier_fishing_encyclopedia.py "C:\path\to\SlotData_0.dat"
```

## What it does

The Fishing Encyclopedia tracks which of the 41 catchable species you've ever reeled in. This data is stored as a **bitfield** inside `SlotData_X.dat` at two mirrored offsets:

| Offset | Size | Description |
|--------|------|-------------|
| `0x3050C` | 4 bytes | 32 species (primary) |
| `0x30512` | 1 byte | 1 species (bit 7) |
| `0x30513` | 1 byte | 8 species |
| `0x385D8` | 4 bytes | Mirror of `0x3050C` |
| `0x385DE` | 1 byte | Mirror of `0x30512` (bit 7 only; other bits belong to other Intel categories) |
| `0x385DF` | 1 byte | Mirror of `0x30513` |

The script sets all fishing bits to `1` and uses OR-masking on shared bytes to avoid affecting other Intel data.

## Safety

- A **backup** (`.bak`) is created automatically before any changes are made.
- The script **only** modifies the 12 bytes listed above — nothing else in your save is touched.
- If the encyclopedia is already at 100%, the script exits without writing anything.

## Species unlocked

All 41 Fishing Encyclopedia entries:

| # | Species | # | Species |
|---|---------|---|---------|
| 1 | Arowana | 22 | Killifish Machine |
| 2 | Twinfish | 23 | Koi Carp Machine |
| 3 | Killifish | 24 | Arapaima Machine |
| 4 | Carp | 25 | Carp Machine |
| 5 | Bloat Fish | 26 | Bloat Fish Machine |
| 6 | Koi Carp | 27 | Blowfish Machine |
| 7 | Fur Carp | 28 | Swordfish Machine |
| 8 | Freshwater Ray | 29 | Starfish Machine |
| 9 | Arapaima | 30 | Bream Machine |
| 10 | Oil Sardine | 31 | Coelacanth Machine |
| 11 | Beetle Fish | 32 | Mackerel Machine |
| 12 | Water Flea | 33 | Horseshoe Crab Machine |
| 13 | Twoface | 34 | Arowana Machine |
| 14 | Coelacanth | 35 | Basking Shark Machine |
| 15 | Blowfish | 36 | Freshwater Ray Machine |
| 16 | Swordfish | 37 | Machine Lifeform Head |
| 17 | Mackerel | 38 | Tire |
| 18 | Horseshoe Crab | 39 | Gas Cylinder |
| 19 | Starfish | 40 | Battery |
| 20 | Bream | 41 | Broken Firearm |
| 21 | Basking Shark | | |

## Compatibility

Tested on the Steam (PC) version of NieR: Automata. Should work with any `SlotData_X.dat` of the standard 235,980-byte size (the script warns if the size differs).

## Credits

Bitfield offsets were identified by binary-diffing multiple save files with known encyclopedia states (0%, 15%, 82%, 85%, 88%, 100%) and confirming each bit with in-game catch verification.

## License

Public domain — do whatever you want with it.
