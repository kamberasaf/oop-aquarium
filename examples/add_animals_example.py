"""Example: add animals to the aquarium programmatically."""
import sys
from pathlib import Path

# Allow running without pip install: add src to path when run from repo root
_root = Path(__file__).resolve().parent.parent
if _root not in sys.path and (_root / "src").exists():
    sys.path.insert(0, str(_root / "src"))

from aquarium import Aqua


def run_example():
    myaqua = Aqua(50, 30)

    success1 = myaqua.add_animal("scalarfish1", 4, 10, 10, 1, 0, "sc")
    print(f"Adding scalarfish1 successful? {success1}")

    success2 = myaqua.add_animal("molyfish2", 12, 35, 15, 0, 1, "mo")
    print(f"Adding molyfish2 successful? {success2}")

    print("\nAquarium board:")
    myaqua.print_board()


if __name__ == "__main__":
    run_example()
