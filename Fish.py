import Animal

MAX_FISH_HEIGHT = 5
MAX_FISH_WIDTH = 8


class Fish(Animal.Animal):

    def __init__(self, name, age, x, y, directionH, directionV):
        super().__init__(name, age, x, y, directionH)
        self.width = MAX_FISH_WIDTH
        self.height = MAX_FISH_HEIGHT
        self.directionV = directionV

    def __str__(self):
        st = "The fish " + str(self.name) + " is " + str(self.age) + " years old and has " + str(self.food) + " food"
        return st

    def up(self):
        self.set_y(self.y-1)

    def down(self):
        self.set_y(self.y+1)

    def starvation(self):
        print(f'the fish {self.name} died at the age of {self.age} years')
        print('Because he ran out of food!')
        self.alive = False

    def die(self):
        self.alive = False

    def get_directionV(self) -> int:
        return self.directionV

    def set_directionV(self, directionV: int):
        self.directionV = directionV