# The OOP Aquarium

An object-oriented Python aquarium simulation featuring four types of animals: two fish types (Scalar and Moly) and two crab types (Ocypode and Shrimp).


## Features

- Add animals with customizable attributes (name, age, location, direction)
- Simulate animal movement in a 2D aquarium environment
- Feed all animals at once
- Step through the simulation turn-by-turn or multiple steps at a time
- Print a live board display of the aquarium state
- Demo mode showcasing the functionality with predefined animals


## Getting Started

### Prerequisites

- Python 3.x installed on your system


### Running the Project

Clone the repository and run the main program:

```bash
git clone https://github.com/kamberasaf/The-OOP-aquarium.git
cd The-OOP-aquarium
python main.py
```


### How to Use
- When prompted, enter the aquarium dimensions (width >= 40, height >= 25)
- Use the main menu to add animals, feed them, advance simulation steps, or run the demo
- Follow input instructions carefully for adding animals (name, age, position, direction)



### Demo

![Aquarium Demo](assets/aquarium_demo.gif)

## Example
```plaintext
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
6. Print all
7. Exit

What do you want to do? 5
```




## Demo

![Aquarium Demo](assets/aquarium_demo.gif)

## Examples
To see how animals can be added programmatically:
```bash
python examples/add_animals_example.py
```


## Running Tests
Tests are located in the tests/ directory and use pytest.
To run the tests:
```bash
pip install pytest
pytest tests/
```


## Quickstart
```bash
python main.py
```

## Programmatic demo
```python
from Aqua import Aqua
aq = Aqua(50,25)
aq.add_animal("scalarfish1", 4, 10, 10, 1, 0, 'sc')
aq.add_animal("molyfish2", 12, 35, 15, 0, 1, 'mo')
aq.add_animal("shrimpcrab1", 3, 20, aq.aqua_height, 1, 0, 'sh')
aq.add_animal("ocypodcrab1", 13, 41, aq.aqua_height, 0, 0, 'oc')
for _ in range(3):
    aq.print_board()
    aq.next_turn()
```


## Tests
Run the unit tests with pytest:

```bash
pytest tests/
```
