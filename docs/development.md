# Development

## Repository layout

```
The-OOP-aquarium/
├── src/
│   └── aquarium/          # Main package
│       ├── __init__.py
│       ├── animal.py      # Base Animal class
│       ├── aqua.py        # Aqua (tank + simulation)
│       ├── crab.py        # Crab base class
│       ├── fish.py        # Fish base class
│       ├── moly.py
│       ├── ocypode.py
│       ├── scalar.py
│       ├── shrimp.py
│       └── utils.py
├── docs/                  # Documentation
│   ├── user_guide.md
│   └── development.md
├── examples/              # Example scripts
├── tests/                 # Pytest tests
├── assets/                # Images (e.g. for README)
├── main.py                # CLI entry point
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Running tests

From the project root:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

Or with `requirements.txt` only:

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/ -v
```

`pyproject.toml` configures pytest to add `src` to `pythonpath`, so the `aquarium` package is found when running tests.

## Adding new animal types

1. Add a new module under `src/aquarium/` that subclasses `fish.Fish` or `crab.Crab`.
2. Implement `get_animal()` returning a list of strings (character grid).
3. In `aqua.py`, extend `add_fish` or `add_crab` to handle a new type code and instantiate your class.
4. Optionally add a menu option in `main.py` for the new type.
