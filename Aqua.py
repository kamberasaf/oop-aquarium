import Animal
import Crab
import Fish
import Moly
import Ocypode
import Scalar
import Shrimp
import main

MAX_ANIMAL_HEIGHT = 8
MAX_ANIMAL_WIDTH = 8
MAX_CRAB_HEIGHT = 4
MAX_CRAB_WIDTH = 7
MAX_FISH_HEIGHT = 5
MAX_FISH_WIDTH = 8
WATERLINE = 3
FEED_AMOUNT = 10
MAX_AGE = 120


class Aqua:
    def __init__(self, aqua_width, aqua_height):
        self.turn = 0
        self.aqua_height = aqua_height
        self.aqua_width = aqua_width
        self.board = [' '] * self.aqua_height
        self.build_tank()
        self.anim = []

    def build_tank(self):
        col, row = self.aqua_width, len(self.board)
        tank = [[' '] * col for _ in range(row)]
        tank[2][1:-1] = '~' * (col - 2)
        tank[-1] = ('_' * (col - 2)).join(['\\', '/'])
        for row in tank[:-1]:
            row[0], row[-1] = '|', '|'
        self.board = tank

    def print_board(self):
        """
        prints the updated board on screen
        """
        for row in self.get_board():
            print(' '.join(item for item in row))

    def get_board(self):
        return self.board

    def get_all_animal(self):
        """
        Returns the array that contains all the animals
        """
        return self.anim

    def is_collision(self, animal: Animal) -> bool:
        """
        Returns True if the next step of the crab is a collision
        """
        x, y = animal.get_position()
        a_dir = animal.get_directionH()
        aq_height = self.aqua_height
        board = self.get_board()
        crabs = [crab for crab in self.get_all_animal() if isinstance(crab, Crab.Crab) is True]
        for crab_2 in crabs:  # we want to look only at crabs.
            if (a_dir == 1 and crab_2.x == x + animal.width) or \
                    (a_dir == 0 and crab_2.x + crab_2.width == x):  # we got a collision.
                self.delete_animal_from_board(crab_2)
                crab_2.set_directionH(1) if crab_2.get_directionH() == 0 else \
                    crab_2.set_directionH(0) if crab_2.get_directionH() == 1 else None
                self.print_animal_on_board(crab_2)

                self.delete_animal_from_board(animal)  # we need to check if our next spot is empty.
                try:
                    if (board[aq_height - 3][x - 1] not in ['|', '*'] and
                            board[aq_height - 4][x - 1] not in ['|', '*']):
                        animal.set_x(x - 1)
                    elif (board[aq_height - 3][x + animal.width + 1] not in ['|', '*'] and
                          board[aq_height - 4][x + animal.width + 1] not in ['|', '*']):
                        animal.set_x(x + 1)
                except IndexError:
                    pass
                animal.set_directionH(0) if a_dir == 1 else \
                    animal.set_directionH(1) if a_dir == 0 else None
                self.print_animal_on_board(animal)
                return True

        return False

    def print_animal_on_board(self, animal: Animal):
        k = animal.get_animal()
        x, y = animal.get_position()
        an_height, an_width = animal.get_size()
        aq_height, aq_width = self.aqua_height, self.aqua_width
        board = self.get_board()
        if isinstance(animal, Fish.Fish):
            if (aq_width - x) < an_width + 1:  # checks if x is too close to right wall.
                animal.set_x(aq_width - an_width - 1)
            board[y][x:x + an_width] = k[0]
            board[y + 1][x:x + an_width] = k[1]
            board[y + 2][x:x + an_width] = k[2]

            if isinstance(animal, Scalar.Scalar):
                board[y + 3][x:x + an_width] = k[3]
                board[y + 4][x:x + an_width] = k[4]

        elif isinstance(animal, Crab.Crab):
            if (aq_width - x) < an_width + 1:  # checks if x is too close to right wall.
                animal.set_x(aq_width - an_width - 1)
            board[aq_height - 4][x:x + an_width] = k[len(k) - 3]
            board[aq_height - 3][x:x + an_width] = k[len(k) - 2]
            board[aq_height - 2][x:x + an_width] = k[len(k) - 1]

            if isinstance(animal, Ocypode.Ocypode):
                board[aq_height - 5][x:x + an_width] = k[0]

    def delete_animal_from_board(self, animal: Animal):
        x, y = animal.get_position()
        an_height, an_width = animal.get_size()
        board = self.get_board()
        aq_height = self.aqua_height
        for h in range(an_height):
            if isinstance(animal, Fish.Fish):
                board[y + h][x:x + an_width] = ' ' * an_width
            else:
                board[aq_height - 2 - h][x:x + an_width] = ' ' * an_width

    def add_animal(self, name, age, x, y, directionH, directionV, animaltype):
        if animaltype == 'sc' or animaltype == 'mo':
            return self.add_fish(name, age, x, y, directionH, directionV, animaltype)
        elif animaltype == 'oc' or animaltype == 'sh':
            return self.add_crab(name, age, x, y, directionH, animaltype)

    def add_fish(self, name, age, x, y, directionH, directionV, fishtype):
        """
        Adding fish to the aquarium
        """
        aq_height, aq_width = self.aqua_height, self.aqua_width
        if (aq_width - x) < MAX_FISH_WIDTH + 1:  # checks if x is too close to right wall.
            x = aq_width - MAX_FISH_WIDTH - 1

        if fishtype == 'sc':  # width - 8, height = 5
            if (aq_height - MAX_ANIMAL_HEIGHT - 1) <= y:
                y = aq_height - MAX_CRAB_HEIGHT - 6
            new_fish = Scalar.Scalar(name, age, x, y, directionH, directionV)
        elif fishtype == 'mo':  # width = 8, height = 3
            if (aq_height - MAX_ANIMAL_HEIGHT) <= y:
                y = aq_height - MAX_CRAB_HEIGHT - 4
            new_fish = Moly.Moly(name, age, x, y, directionH, directionV)

        if not self.check_if_free(x, y):  # check if we get an 8x8 cube of free space.
            print("The place is not available! Please try again later. ")
            return False

        self.anim.append(new_fish)
        self.print_animal_on_board(new_fish)
        return True

    def add_crab(self, name, age, x, y, directionH, crabtype):
        """
        Adding crab to the aquarium
        """
        if (self.aqua_width - x) < MAX_CRAB_WIDTH + 1:  # checks if x is too close to right wall.
            x = self.aqua_width - MAX_CRAB_WIDTH - 1
        y = self.aqua_height - MAX_CRAB_HEIGHT

        if not self.check_if_free(x, y):
            print("The place is not available! Please try again later. ")
            return False

        if crabtype == 'sh':  # shrimp
            new_crab = Shrimp.Shrimp(name, age, x, y, directionH)
        elif crabtype == 'oc':  # ocypode
            new_crab = Ocypode.Ocypode(name, age, x, y, directionH)
        self.anim.append(new_crab)
        self.print_animal_on_board(new_crab)
        return True
    def check_if_free(self, x: int, y: int) -> bool:
        """Check an area starting at (x,y) is free for the next animal's footprint.
        Uses a conservative MAX footprint to avoid overlap.
        """
        try:
            # Fallback to conservative max footprint if next animal size is unknown at callsite
            h, w = MAX_ANIMAL_HEIGHT, MAX_ANIMAL_WIDTH
            for t in range(h):
                # Guard bounds
                if y + t < 0 or y + t >= self.aqua_height:
                    continue
                row = self.board[y + t]
                x0, x1 = max(0, x), min(self.aqua_width, x + w)
                if '*' in row[x0:x1]:
                    return False
        except IndexError:
            # Out of bounds means not placeable
            return False
        return True


    def left(self, a: Animal):
        animal = a
        x, y = animal.get_position()
        if self.board[y][x - 1] == '|':  # first we check if we hit a wall on the next move.
            self.delete_animal_from_board(animal)
            animal.set_directionH(1)
            return self.print_animal_on_board(animal)

        if isinstance(animal, Crab.Crab):
            if self.is_collision(animal):  # this function will handle crabs collisions.
                return None

        self.delete_animal_from_board(animal)
        animal.left()
        self.print_animal_on_board(animal)

    def right(self, a: Animal):
        animal = a
        x, y = animal.get_position()
        if (isinstance(animal, Crab.Crab) and self.board[y][x + animal.width] == '|') or \
                (isinstance(animal, Fish.Fish) and self.board[y][x + animal.width] == '|'):
            self.delete_animal_from_board(animal)  # if it's a wall just turn around
            animal.set_directionH(0)
            return self.print_animal_on_board(animal)

        if isinstance(animal, Crab.Crab):
            if self.is_collision(animal):  # this will handle crabs collisions.
                return None

        self.delete_animal_from_board(animal)
        animal.right()
        self.print_animal_on_board(animal)

    def up(self, a: Animal):
        fish = a
        x, y = fish.get_position()
        if y == WATERLINE:
            self.delete_animal_from_board(fish)
            fish.set_directionV(0)
            return self.print_animal_on_board(fish)

        self.delete_animal_from_board(fish)
        fish.up()
        self.print_animal_on_board(fish)

    def down(self, a: Animal):
        fish = a
        x, y = fish.get_position()
        bottom = self.aqua_height - MAX_CRAB_HEIGHT - 1
        if y + fish.height >= bottom:
            fish.set_directionV(1)
            self.delete_animal_from_board(fish)
            self.print_animal_on_board(fish)
            return None

        self.delete_animal_from_board(fish)
        fish.down()
        self.print_animal_on_board(fish)

    def next_turn(self):
        """
        Managing a single step
        """
        for animal in self.anim[:]:
            if self.turn % 10 == 0:
                animal.dec_food()
                if self.turn % 100 == 0:
                    animal.inc_age()

                if not animal.get_alive():  # check if the fish has died.
                    self.delete_animal_from_board(animal)
                    self.anim.remove(animal)
                    continue

            try:
                if animal.get_directionV() == 0:
                    self.down(animal)
                else:
                    self.up(animal)
            except AttributeError:
                pass

            if animal.get_directionH() == 1:
                self.right(animal)
                if animal.get_directionH() == 0:  # skip if the animal has changed direction.
                    continue
            else:
                self.left(animal)

        for anim in self.anim:  # make sure the animals are not missing body parts.
            self.delete_animal_from_board(anim)
            self.print_animal_on_board(anim)

        self.turn += 1

    def print_all(self):
        """
        Prints all the animals in the aquarium
        """
        for animal in self.anim:
            print(animal)

    def feed_all(self):
        """
        feed all the animals in the aquarium
        """
        for animal in self.get_all_animal():
            animal.add_food(FEED_AMOUNT)

    def several_steps(self):
        """
        Managing several steps
        """
        num_of_steps = 0
        valid_input = False
        while not valid_input:
            num_of_steps = input('How many step do you want to take?')
            num_of_steps = main.valid_num_check(num_of_steps)
            if not num_of_steps:
                continue
            valid_input = True

        for i in range(num_of_steps):
            self.next_turn()