# The OOP Aquarium

An object-oriented Python aquarium simulation featuring four types of animals: two fish (Scalar and Moly) and two crabs (Ocypode and Shrimp).

## Features

- **Add animals** with name, age, and direction; **interactive placement** shows the real fish/crab sprite — move with arrow keys, Enter to place, ESC to cancel
- Simulate animal movement in a 2D aquarium (fish swim, crabs walk on the bottom)
- Feed all animals at once; hunger bar and name/age shown above and below each animal
- Step through the simulation turn-by-turn or take several steps (with optional P to pause, Q to quit)
- **List all animals** (name, age, food) — printed below the aquarium after each menu action
- **Demo mode** — random mix of 2–6 animals, random positions and directions; runs for 120 steps with automatic feeding; **P** to pause, **Q** to quit
- **Reset** — remove all animals and start with an empty tank

## Demo

![Aquarium Demo](assets/aquarium_demo.gif)

The demo creates a random set of animals (Scalar, Moly, Ocypode, Shrimp) with random names, ages, and positions. During the demo you can press **P** to pause and **Q** to quit.

## Repository structure

| Path | Description |
|------|--------------|
| **`src/aquarium/`** | Main Python package (aquarium logic, animals, utils) |
| **`docs/`** | Documentation ([user guide](docs/user_guide.md), [development](docs/development.md)) |
| **`examples/`** | Example scripts |
| **`tests/`** | Pytest tests |
| **`assets/`** | Images and media (e.g. for README) |
| **`main.py`** | CLI entry point |

## Getting Started

### Prerequisites

- **Python 3.9+**

### Installation

```bash
git clone https://github.com/kamberasaf/The-OOP-aquarium.git
cd The-OOP-aquarium
pip install -r requirements.txt
pip install -e .
```

The last line installs the `aquarium` package in editable mode so you can run the app and tests. If you only want to run the CLI without installing, ensure you run from the project root and have installed dependencies (see [Development](docs/development.md)).

### Run the application

```bash
python main.py
```

- Enter aquarium dimensions when prompted (width ≥ 40, height ≥ 25).
- Use the menu to add animals, feed them, advance steps, run the demo, list animals, or reset the tank.
- When adding an animal, you choose type and name/age/direction, then **place it interactively**: the aquarium is shown with the actual animal sprite; use **arrow keys** to move, **Enter** to place, **ESC** to cancel.

### Example session

```text
Welcome to "The OOP Aquarium"
The width of the aquarium (Minimum 40): 50
The height of the aquarium (Minimum 25): 30

Main menu
------------------------------
1. Add an animal
2. Drop food into the aquarium
3. Take a step forward
4. Take several steps
5. Demo
6. List all animals (name, age, food)
7. Exit
8. Reset (remove all animals)

(Type 1–8 or a command: add animal, food, demo, reset, exit.)
What do you want to do? 5
```

Option **6** prints the list of all animals *below* the aquarium. Option **5** (Demo) runs a randomized simulation; press **P** to pause, **Q** to quit.

## Programmatic usage

Run the included example:

```bash
python examples/add_animals_example.py
```

Or use the API in your own script (after `pip install -e .`):

```python
from aquarium import Aqua

aq = Aqua(50, 25)
aq.add_animal("scalarfish1", 4, 10, 10, 1, 0, "sc")
aq.add_animal("molyfish2", 12, 35, 15, 0, 1, "mo")
aq.add_animal("shrimpcrab1", 3, 20, aq.aqua_height, 1, 0, "sh")
aq.add_animal("ocypodcrab1", 13, 41, aq.aqua_height, 0, 0, "oc")
for _ in range(3):
    aq.print_board()
    aq.next_turn()
```

Animal type codes: `sc` (Scalar), `mo` (Moly), `oc` (Ocypode), `sh` (Shrimp).

More details: [docs/user_guide.md](docs/user_guide.md).

## Tests

From the project root:

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/ -v
```

## Documentation

- [User guide](docs/user_guide.md) — running the app and using the API
- [Development](docs/development.md) — repo layout, running tests, extending the project
