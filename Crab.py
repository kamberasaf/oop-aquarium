import Animal

MAX_CRAB_HEIGHT = 4
MAX_CRAB_WIDTH = 7


class Crab(Animal.Animal):
    def __init__(self, name, age, x, y, directionH):
        super().__init__(name, age, x, y, directionH)

    def __str__(self):
        st = "The crab " + str(self.name) + " is " + str(self.age) + " years old and has " + str(self.food) + " food"
        return st

    def starvation(self):
        self.alive = False
        print(f'the crab {self.name} died at the age of {self.age} years')
        print('Because he ran out of food!')

    def die(self):
        self.alive = False
        print(f'{self.name} died in good health')