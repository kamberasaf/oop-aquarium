import random
import sys
import time
from pathlib import Path

# Allow running from repo root without pip install
_root = Path(__file__).resolve().parent
if _root not in sys.path and (_root / "src").exists():
    sys.path.insert(0, str(_root / "src"))

from aquarium import Aqua, WATERLINE
from aquarium.config import (
    ANIMAL_TYPES,
    DEMO_FEED_INTERVAL,
    DEMO_SLEEP_SECONDS,
    DEMO_TOTAL_STEPS,
    FEED_AMOUNT,
    MAX_AGE_INPUT,
    MIN_AGE_INPUT,
    MIN_TANK_HEIGHT,
    MIN_TANK_WIDTH,
    STEP_DELAY_SECONDS,
    TURNS_PER_FOOD_DECREMENT,
    WATERLINE,
    fish_lowest_y,
)
from aquarium.placement import run_placement
from aquarium.terminal_io import (
    KEY_DOWN,
    KEY_ENTER,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_UP,
    clear_screen,
    flush_stdin,
    get_key,
    try_get_key,
)
from aquarium.utils import valid_num_check

# Random demo: name pool and count range
_DEMO_NAMES = (
    "Nemo", "Bubbles", "Finley", "Coral", "Shelly", "Claw", "Moti", "Nami",
    "Splash", "Finn", "Pearl", "Shadow", "Crabby", "Pincher", "Skipper", "Dory",
)
_DEMO_MIN_ANIMALS = 2
_DEMO_MAX_ANIMALS = 6
_DEMO_PLACEMENT_ATTEMPTS = 15


def _parse_horizontal(s: str) -> int | None:
    """Parse horizontal direction: 0=Left, 1=Right. Returns 0 or 1 or None."""
    s = (s or "").strip().lower()
    if s in ("0", "l", "left"):
        return 0
    if s in ("1", "r", "right"):
        return 1
    return None


def _parse_vertical(s: str) -> int | None:
    """Parse vertical direction: 0=Down, 1=Up. Returns 0 or 1 or None."""
    s = (s or "").strip().lower()
    if s in ("0", "d", "down"):
        return 0
    if s in ("1", "u", "up"):
        return 1
    return None


def _get_direction_horizontal() -> int:
    """Prompt for horizontal direction; accept arrow key or R/L/Left/Right/0/1."""
    while True:
        print("Horizontal direction: press Left/Right arrow, or type L/R/Left/Right/0/1: ", end="", flush=True)
        key = get_key()
        if key in (KEY_LEFT, "l", "0"):
            flush_stdin()
            return 0
        if key in (KEY_RIGHT, "r", "1"):
            flush_stdin()
            return 1
        if key == KEY_ENTER:
            line = input("Type L/R/Left/Right/0/1: ").strip()
            val = _parse_horizontal(line)
            if val is not None:
                return val
        else:
            flush_stdin()
        print("Invalid. Use Left/Right arrow, or L/R/Left/Right/0/1.\n")


def _get_direction_vertical() -> int:
    """Prompt for vertical direction; accept arrow key or D/U/Down/Up/0/1."""
    while True:
        print("Vertical direction: press Up/Down arrow, or type D/U/Down/Up/0/1: ", end="", flush=True)
        key = get_key()
        if key in (KEY_DOWN, "d", "0"):
            flush_stdin()
            return 0
        if key in (KEY_UP, "u", "1"):
            flush_stdin()
            return 1
        if key == KEY_ENTER:
            line = input("Type D/U/Down/Up/0/1: ").strip()
            val = _parse_vertical(line)
            if val is not None:
                return val
        else:
            flush_stdin()
        print("Invalid. Use Up/Down arrow, or D/U/Down/Up/0/1.\n")


def do_feed(myaqua):
    """Drop food and show clear feedback for each animal."""
    animals = list(myaqua.get_all_animal())
    if not animals:
        print("\nNo animals in the aquarium. Add some first!\n")
        return
    old_food = {a.name: a.get_food() for a in animals}
    myaqua.feed_all()
    print(f"\nFood dropped! +{FEED_AMOUNT} food each.")
    print(f"(Animals lose 1 food every {TURNS_PER_FOOD_DECREMENT} steps; at 0 they starve.)\n")
    print("Fed:\n")
    for a in animals:
        print(f"  {a.name}: {old_food[a.name]} → {a.get_food()} food")
    print()


def parse_menu_choice(raw: str, valid_numbers: set) -> int | bool:
    """
    Parse menu input: number 1-7 or text command.
    Returns the option number (1-7) or False if invalid.
    """
    s = (raw or "").strip().lower()
    if not s:
        return False
    # Numeric input
    try:
        n = int(s)
        return n if n in valid_numbers else False
    except ValueError:
        pass
    # Text commands (check longer / more specific first)
    words = set(s.split())
    if "several" in words or "steps" in words:
        return 4 if 4 in valid_numbers else False
    if "step" in words:
        return 3 if 3 in valid_numbers else False
    if "add" in words or "animal" in words:
        return 1 if 1 in valid_numbers else False
    if "food" in words or "feed" in words or "drop" in words:
        return 2 if 2 in valid_numbers else False
    if "demo" in words:
        return 5 if 5 in valid_numbers else False
    if "print" in words or "list" in words:
        return 6 if 6 in valid_numbers else False
    if "exit" in words or "quit" in words:
        return 7 if 7 in valid_numbers else False
    if "reset" in words or "flush" in words or "clear" in words:
        return 8 if 8 in valid_numbers else False
    return False


def _random_demo_animals(myaqua):
    """Generate random animals and add them to the aquarium."""
    aq_w, aq_h = myaqua.aqua_width, myaqua.aqua_height
    fish_bottom = fish_lowest_y(aq_h)
    codes = ["sc", "mo", "oc", "sh"]
    # Valid x for all (crab/fish width up to 8)
    x_min, x_max = 1, max(1, aq_w - 8 - 1)
    names_used = set()

    def pick_name():
        for _ in range(20):
            name = random.choice(_DEMO_NAMES)
            if name not in names_used:
                names_used.add(name)
                return name
            name = f"{random.choice(_DEMO_NAMES)}{random.randint(1, 99)}"
            if name not in names_used:
                names_used.add(name)
                return name
        return f"Animal{random.randint(1, 999)}"

    n = random.randint(_DEMO_MIN_ANIMALS, _DEMO_MAX_ANIMALS)
    added = 0
    for _ in range(n * 3):  # allow retries
        if added >= n:
            break
        code = random.choice(codes)
        name = pick_name()
        age = random.randint(1, 20)
        dir_h = random.randint(0, 1)
        dir_v = random.randint(0, 1) if code in ("sc", "mo") else 0
        x = random.randint(x_min, x_max) if x_max >= x_min else x_min
        if code in ("sc", "mo"):
            y_min = WATERLINE
            y_max = max(y_min, fish_bottom - 5)
            y = random.randint(y_min, y_max) if y_max >= y_min else y_min
        else:
            y = myaqua.aqua_height - 4
        if myaqua.add_animal(name, age, x, y, dir_h, dir_v, code):
            added += 1


def demo(myaqua):
    myaqua.reset()
    _random_demo_animals(myaqua)
    clear_screen()
    myaqua.print_board()
    print("\nDemo running. Press P to pause, Q to quit demo.\n")

    for i in range(DEMO_TOTAL_STEPS):
        key = try_get_key()
        if key == "q":
            print("Demo stopped.")
            flush_stdin()
            return
        if key == "p":
            flush_stdin()
            print("  [Paused. Press P to resume.]")
            while True:
                time.sleep(0.1)
                k = try_get_key()
                if k == "p":
                    flush_stdin()
                    break
                if k == "q":
                    flush_stdin()
                    print("Demo stopped.")
                    return
            clear_screen()
            myaqua.print_board()
            print("\nDemo running. Press P to pause, Q to quit demo.\n")

        if i % DEMO_FEED_INTERVAL == 0:
            myaqua.feed_all()
        myaqua.next_turn()
        if i != DEMO_TOTAL_STEPS - 1:
            clear_screen()
            myaqua.print_board()
            print("\nDemo running. Press P to pause, Q to quit demo.\n")
        time.sleep(DEMO_SLEEP_SECONDS)


def add_animal(myaqua):
    valid_int = False
    while not valid_int:
        print("\nPlease select:")
        for idx, info in enumerate(ANIMAL_TYPES, start=1):
            print(f"{idx}. {info.label}")
        choice = input("What animal do you want to put in the aquarium?")
        choice = valid_num_check(choice)
        if choice not in range(1, len(ANIMAL_TYPES) + 1):
            if choice:
                print("\nPlease enter a valid number.\n")
            continue
        valid_int = True
        selected = ANIMAL_TYPES[choice - 1]

    valid_name = False
    while not valid_name:
        name = input("Please enter a name:")
        try:
            stripped = name.replace(" ", "")
            if not stripped or not all(c.isalnum() for c in stripped):
                raise ValueError
        except (ValueError, TypeError):
            print("\nPlease enter a valid name.")
            continue
        valid_name = True

    valid_age = False
    while not valid_age:
        age = input("Please enter age:")
        age = valid_num_check(age)
        if age is False or not (MIN_AGE_INPUT <= age <= MAX_AGE_INPUT):
            if age is not False:
                print("\nPlease enter a valid number.\n")
            continue
        valid_age = True

    directionH = _get_direction_horizontal()

    if selected.is_fish:
        directionV = _get_direction_vertical()
    else:
        directionV = 0

    # Interactive placement: show aquarium with moving X, Enter to place, ESC to cancel
    result = run_placement(myaqua, selected.code)
    if result is None:
        print("Cancelled.")
        return None
    x, y = result
    myaqua.add_animal(name, age, x, y, directionH, directionV, selected.code)
    return None


def do_several_steps(myaqua):
    """Run N steps and show each one (movement, collisions, feeding) with a short delay."""
    valid_input = False
    while not valid_input:
        num_of_steps = input("How many steps do you want to take? ")
        num_of_steps = valid_num_check(num_of_steps)
        if num_of_steps is False or not num_of_steps:
            continue
        valid_input = True

    for i in range(num_of_steps):
        key = try_get_key()
        if key == "q":
            print("Stopped early.")
            flush_stdin()
            return
        if key == "p":
            flush_stdin()
            print("  [Paused. Press P to resume, Q to quit.]")
            while True:
                time.sleep(0.1)
                k = try_get_key()
                if k == "p":
                    flush_stdin()
                    break
                if k == "q":
                    flush_stdin()
                    print("Stopped.")
                    return

        myaqua.next_turn()
        clear_screen()
        myaqua.print_board()
        print(f"\nStep {i + 1} of {num_of_steps}. P=pause, Q=quit\n")
        time.sleep(STEP_DELAY_SECONDS)


def main():
    print('\nWelcome to "The OOP Aquarium"')
    valid_input = False
    while not valid_input:
        width = input(f"The width of the aquarium (Minimum {MIN_TANK_WIDTH}): ")
        width = valid_num_check(width, MIN_TANK_WIDTH)
        if width is False:
            continue
        valid_height = False
        while not valid_height:
            height = input(f"The height of the aquarium (Minimum {MIN_TANK_HEIGHT}): ")
            height = valid_num_check(height, MIN_TANK_HEIGHT)
            if height is False:
                continue
            valid_height = True
        valid_input = True

    myaqua = Aqua(width, height)

    def do_reset():
        myaqua.reset()

    menu_options = [
        (1, "Add an animal", lambda: add_animal(myaqua)),
        (2, "Drop food into the aquarium", lambda: do_feed(myaqua)),
        (3, "Take a step forward", myaqua.next_turn),
        (4, "Take several steps", lambda: do_several_steps(myaqua)),
        (5, "Demo", lambda: demo(myaqua)),
        (6, "List all animals (name, age, food)", lambda: None),  # list printed after aquarium below
        (7, "Exit", None),
        (8, "Reset (remove all animals)", do_reset),
    ]
    valid_choices = {opt[0] for opt in menu_options}

    while True:
        valid_input = False
        while not valid_input:
            print("\nMain menu")
            print("-" * 30)
            for num, label, _ in menu_options:
                print(f"{num}. {label}")
            print("(Type 1–8 or a command: add animal, food, demo, reset, exit.)")
            print("Tags: Name (Age) [*****] (N) — bar = hunger (*=1 food, .=empty), (N)=current food.")
            raw = input("\nWhat do you want to do? ")
            choice = parse_menu_choice(raw, valid_choices)
            if choice is False:
                print("\nUnknown option. Use 1–8 or a command (e.g. add animal, food, demo, reset).\n")
                continue
            valid_input = True

        action = next(a[2] for a in menu_options if a[0] == choice)
        if action is None:
            print("Bye bye")
            break
        if callable(action):
            action()

        clear_screen()
        if choice == 8:
            print("All animals removed. Aquarium reset.\n")
        myaqua.print_board()
        print("\n")
        if choice == 6:
            animals = list(myaqua.get_all_animal())
            if not animals:
                print("No animals in the aquarium. Add some first!")
            else:
                myaqua.print_all()
            print()


if __name__ == "__main__":
    main()
