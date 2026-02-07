# User Guide

This document describes how to use The OOP Aquarium from the command line and from Python.

## Running the application

From the project root after [installation](../README.md#installation):

```bash
python main.py
```

You will be asked for:

- **Aquarium dimensions**: width (minimum 40) and height (minimum 25).
- **Menu choices**: add animals, feed, step, demo, print, or exit.

## Menu options

| Option | Description |
|--------|-------------|
| 1. Add an animal | Add a Scalar, Moly, Ocypode, or Shrimp with name, age, position, and direction |
| 2. Drop food | Add food for all animals |
| 3. Take a step forward | Advance the simulation by one turn |
| 4. Take several steps | Advance by a number of turns you choose |
| 5. Demo | Run the built-in demo (predefined animals, automatic steps) |
| 6. Print all | List all animals and their state |
| 7. Exit | Quit the program |

## Animal types

- **Scalar** (`sc`) — Fish, 8×5 character sprite  
- **Moly** (`mo`) — Fish, 8×3  
- **Ocypode** (`oc`) — Crab, 7×4  
- **Shrimp** (`sh`) — Crab, 7×3  

Fish swim in the water; crabs stay on the bottom. Directions: horizontal 0 = left, 1 = right; vertical (fish only) 0 = down, 1 = up.

## Programmatic usage

Install the package in editable mode so the `aquarium` package is available:

```bash
pip install -e .
```

Then in Python:

```python
from aquarium import Aqua

aq = Aqua(50, 25)
aq.add_animal("scalar1", 4, 10, 10, 1, 0, "sc")
aq.add_animal("moly1", 12, 35, 15, 0, 1, "mo")
aq.feed_all()
aq.next_turn()
aq.print_board()
```

See the [README](../README.md#programmatic-usage) for more examples.
