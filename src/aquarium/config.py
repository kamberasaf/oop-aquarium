"""
Central configuration for the aquarium simulation.

All tunable constants and type metadata live here so the rest of the code
stays free of magic numbers and is easy to change or extend.
"""

from __future__ import annotations

from typing import NamedTuple

# -----------------------------------------------------------------------------
# Tank / board
# -----------------------------------------------------------------------------
MIN_TANK_WIDTH = 40
MIN_TANK_HEIGHT = 25

# Row index where the water surface is drawn (0-based). Fish cannot go above this.
WATERLINE_ROW = 3
# Number of rows reserved for the floor at the bottom (e.g. the \___/ line).
FLOOR_ROW_OFFSET = 1

# For compatibility: WATERLINE as a name used elsewhere (y-coordinate = waterline row).
WATERLINE = WATERLINE_ROW

# -----------------------------------------------------------------------------
# Simulation (turn-based rules)
# -----------------------------------------------------------------------------
# Every N turns, each animal loses 1 food.
TURNS_PER_FOOD_DECREMENT = 10
# Every N turns, each animal ages by 1 year.
TURNS_PER_AGE_INCREMENT = 100
# Maximum age in years; animal dies when reached.
MAX_AGE = 120
# Food units added when feeding all animals.
FEED_AMOUNT = 10
# Number of segments in the hunger bar shown on name tags (● = fed, ○ = empty).
HUNGER_BAR_LENGTH = 5

# -----------------------------------------------------------------------------
# Animal defaults and size bounds
# -----------------------------------------------------------------------------
STARTING_FOOD = 5
# Conservative max footprint used for collision/placement checks (must fit any animal).
MAX_ANIMAL_HEIGHT = 8
MAX_ANIMAL_WIDTH = 8

# Fish size bounds (any fish fits within this).
MAX_FISH_HEIGHT = 5
MAX_FISH_WIDTH = 8
# Crab size bounds (any crab fits within this).
MAX_CRAB_HEIGHT = 4
MAX_CRAB_WIDTH = 7

# -----------------------------------------------------------------------------
# Per-species dimensions (used by concrete animal classes)
# -----------------------------------------------------------------------------
SCALAR_WIDTH = 8
SCALAR_HEIGHT = 5
MOLY_WIDTH = 8
MOLY_HEIGHT = 3
OCYPODE_WIDTH = 7
OCYPODE_HEIGHT = 4
SHRIMP_WIDTH = 7
SHRIMP_HEIGHT = 3

# -----------------------------------------------------------------------------
# CLI / UI (main.py, demo)
# -----------------------------------------------------------------------------
MIN_AGE_INPUT = 1
MAX_AGE_INPUT = 100
# Demo mode: total steps and how often to feed (every N steps).
DEMO_TOTAL_STEPS = 120
DEMO_FEED_INTERVAL = 50
DEMO_SLEEP_SECONDS = 0.5
# Delay between steps when running "Take several steps" (so you see movement).
STEP_DELAY_SECONDS = 0.4

# Direction constants (0 = left/down, 1 = right/up) for clarity in code.
DIR_LEFT = 0
DIR_RIGHT = 1
DIR_DOWN = 0
DIR_UP = 1


class AnimalTypeInfo(NamedTuple):
    """Metadata for one animal type in the menu."""
    code: str       # e.g. 'sc', 'mo'
    label: str      # e.g. 'Scalar', 'Moly'
    is_fish: bool   # True -> ask vertical direction and use directionV


# Menu order: (menu number 1-based, type code, label, is_fish).
# Main uses this to drive prompts and add_animal calls.
ANIMAL_TYPES = (
    AnimalTypeInfo("sc", "Scalar", True),
    AnimalTypeInfo("mo", "Moly", True),
    AnimalTypeInfo("oc", "Ocypode", False),
    AnimalTypeInfo("sh", "Shrimp", False),
)


def content_bottom_row(aqua_height: int) -> int:
    """Row index of the last content row (just above the floor)."""
    return aqua_height - FLOOR_ROW_OFFSET - 1


def crab_row_index(aqua_height: int, crab_height: int, row_from_top: int) -> int:
    """Board row index for a crab line. row_from_top is 0-based (0 = top of crab)."""
    bottom = content_bottom_row(aqua_height)
    return bottom - (crab_height - 1) + row_from_top


def crab_zone_top_row(aqua_height: int) -> int:
    """Top row index of the crab zone (used for collision escape checks)."""
    return aqua_height - MAX_CRAB_HEIGHT - 1


def fish_lowest_y(aqua_height: int) -> int:
    """Lowest y-coordinate (row) a fish can occupy (bottom of water column)."""
    return aqua_height - MAX_CRAB_HEIGHT - 1
