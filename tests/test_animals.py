from aquarium import Aqua

def test_add_animal():
    aquarium = Aqua(50, 30)
    result = aquarium.add_animal("TestFish", 5, 10, 10, 1, 0, 'sc')
    assert result is True, "Failed to add a valid animal"

def test_invalid_animal():
    aquarium = Aqua(50, 30)
    result = aquarium.add_animal("", -1, 0, 0, -1, -1, 'xx')
    assert result is False, "Invalid animal was incorrectly added"
