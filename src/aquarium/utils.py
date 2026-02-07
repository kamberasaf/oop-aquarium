"""Shared utilities for The OOP Aquarium."""
from __future__ import annotations


def valid_num_check(word: str, minimum: int = 0) -> int | bool:
    """
    Parse and validate a string as an integer >= minimum.
    Returns the integer on success, False on invalid input.
    """
    try:
        if "." in word:
            fractional = word.split(".")[1]
            if any(c != "0" for c in fractional):
                print("\nPlease enter a valid number.\n")
                return False
        value = int(float(word))
        if value < minimum or value <= 0:
            raise ValueError
        return value
    except (ValueError, TypeError):
        print("\nPlease enter a valid number.\n")
        return False
