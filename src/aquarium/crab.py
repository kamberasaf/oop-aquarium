from . import animal, config


class Crab(animal.Animal):
    def __init__(self, name, age, x, y, directionH):
        super().__init__(name, age, x, y, directionH)
        self.width = config.MAX_CRAB_WIDTH
        self.height = config.MAX_CRAB_HEIGHT

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
