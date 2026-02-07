"""
Interactive placement: show the aquarium with the actual animal sprite as cursor.
User moves with arrow keys, Enter to place, ESC to cancel.
"""

from __future__ import annotations

from . import config, moly, ocypode, scalar, shrimp
from .terminal_io import KEY_DOWN, KEY_ENTER, KEY_ESCAPE, KEY_LEFT, KEY_RIGHT, KEY_UP, clear_screen, get_key


# Placement dimensions and bounds by type code
_PLACEMENT = {
    "sc": (config.SCALAR_WIDTH, config.SCALAR_HEIGHT, True),
    "mo": (config.MOLY_WIDTH, config.MOLY_HEIGHT, True),
    "oc": (config.OCYPODE_WIDTH, config.OCYPODE_HEIGHT, False),
    "sh": (config.SHRIMP_WIDTH, config.SHRIMP_HEIGHT, False),
}


def _get_placement_sprite(code: str) -> tuple[list[str], int, int]:
    """Return (sprite lines, width, height) for the animal type. Sprite faces right."""
    w, h, _ = _PLACEMENT[code]
    if code == "sc":
        a = scalar.Scalar("", 0, 0, 0, config.DIR_RIGHT, 0)
    elif code == "mo":
        a = moly.Moly("", 0, 0, 0, config.DIR_RIGHT, 0)
    elif code == "oc":
        a = ocypode.Ocypode("", 0, 0, 0, config.DIR_RIGHT)
    elif code == "sh":
        a = shrimp.Shrimp("", 0, 0, 0, config.DIR_RIGHT)
    else:
        return ([], w, h)
    return (a.get_animal(), w, h)


def _bounds(aqua, code: str):
    """Return (width, height, x_min, x_max, y_min, y_max, cursor_y_for_crab)."""
    w, h, is_fish = _PLACEMENT[code]
    aq_w = aqua.aqua_width
    aq_h = aqua.aqua_height
    x_min = 1
    x_max = max(1, aq_w - w - 1)
    if is_fish:
        fish_bottom = config.fish_lowest_y(aq_h)
        y_min = config.WATERLINE
        y_max = max(y_min, fish_bottom - h)
        return w, h, x_min, x_max, y_min, y_max, None
    else:
        # Crab: y is fixed; we only move x. Use same row logic as aqua._crab_row.
        crab_top = config.crab_row_index(aq_h, h, 0)
        return w, h, x_min, x_max, crab_top, crab_top, crab_top


def _draw_board_with_cursor(
    aqua, cursor_x: int, cursor_y: int, can_place: bool,
    sprite: list[str], w: int, h: int, is_fish: bool,
    animal_type_code: str,
) -> None:
    """Print the aquarium board with the placement sprite drawn at (cursor_x, cursor_y)."""
    lines, line_to_board_row = aqua.get_display_lines()
    # Map board row index -> display line index (for the actual board row line, not labels)
    row_to_line = {r: i for i, r in enumerate(line_to_board_row) if r >= 0}
    for sr in range(h):
        board_row = (cursor_y + sr) if is_fish else aqua._crab_row(sr, h)
        i = row_to_line.get(board_row)
        if i is None:
            continue
        line_list = list(lines[i])
        for j in range(w):
            idx = 2 * (cursor_x + j)
            if idx < len(line_list):
                line_list[idx] = sprite[sr][j]
        lines[i] = "".join(line_list)
    for line in lines:
        print(line)
    type_name = next((t.name for t in config.ANIMAL_TYPES if t.code == animal_type_code), animal_type_code)
    if can_place:
        status = f"  Placing {type_name}: [OK - space free]  Enter to place"
    else:
        status = f"  Placing {type_name}: [No room here]  Move to a free spot"
    print(status)


def run_placement(aqua, animal_type_code: str) -> tuple[int, int] | None:
    """
    Interactive placement: show aquarium with actual animal sprite; move with arrow keys, Enter to place, ESC to cancel.
    Returns (x, y) on confirm, or None if user cancels.
    """
    w, h, x_min, x_max, y_min, y_max, crab_cursor_y = _bounds(aqua, animal_type_code)
    is_fish = animal_type_code in ("sc", "mo")
    sprite, sprite_w, sprite_h = _get_placement_sprite(animal_type_code)

    # Initial cursor: middle of valid range
    cursor_x = max(x_min, min(x_max, (x_min + x_max) // 2))
    cursor_y = y_min if is_fish else crab_cursor_y

    while True:
        clear_screen()
        can_place = aqua.check_if_free(cursor_x, cursor_y, width=w, height=h)
        _draw_board_with_cursor(aqua, cursor_x, cursor_y, can_place, sprite, sprite_w, sprite_h, is_fish, animal_type_code)
        print()
        print("  Arrow keys: move  |  Enter: place here  |  ESC: cancel")
        print()

        key = get_key()
        if key == KEY_ESCAPE:
            return None
        if key == KEY_ENTER:
            if can_place:
                return (cursor_x, cursor_y)
            # Stay in loop so user can move and try again
            continue
        if key == KEY_LEFT and cursor_x > x_min:
            cursor_x -= 1
        elif key == KEY_RIGHT and cursor_x < x_max:
            cursor_x += 1
        elif key == KEY_UP and is_fish and cursor_y > y_min:
            cursor_y -= 1
        elif key == KEY_DOWN and is_fish and cursor_y < y_max:
            cursor_y += 1
