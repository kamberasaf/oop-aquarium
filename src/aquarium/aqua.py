from __future__ import annotations

from . import animal, config, crab, fish, moly, ocypode, scalar, shrimp
from .utils import valid_num_check


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
        tank[config.WATERLINE_ROW][1:-1] = '~' * (col - 2)
        tank[-1] = ('_' * (col - 2)).join(['\\', '/'])
        for r in tank[:-1]:
            r[0], r[-1] = '|', '|'
        self.board = tank

    def _animal_top_row(self, a: animal.Animal) -> int:
        """Board row index of the top of this animal's sprite."""
        x, y = a.get_position()
        an_height, _ = a.get_size()
        if isinstance(a, fish.Fish):
            return y
        return self._crab_row(0, an_height)

    def get_display_lines(self) -> tuple[list[str], list[int]]:
        """
        Build board display: hunger/food above each animal, name+age below.
        Returns (list of display lines, list mapping display line index -> board row, or -1 for label lines).
        """
        board = self.get_board()
        aq_width = self.aqua_width
        labels_at_row = {}
        for a in self.anim:
            if not a.get_alive():
                continue
            top_row = self._animal_top_row(a)
            height, _ = a.get_size()
            x, _ = a.get_position()
            food = a.get_food()
            filled = min(config.HUNGER_BAR_LENGTH, max(0, food))
            hunger_bar = "*" * filled + "." * (config.HUNGER_BAR_LENGTH - filled)
            # Hunger/food above the animal (label line inserted before animal's first row)
            if top_row >= 0:
                labels_at_row.setdefault(top_row, []).append((x, f"[{hunger_bar}] ({food})"))
            # Name + age below the animal (only if above the floor)
            label_below = top_row + height
            if label_below < self.aqua_height - 1:
                labels_at_row.setdefault(label_below, []).append((x, f"{a.name} ({a.get_age()})"))
            # Crabs sit on the floor: show name+age above them (row below is the floor)
            elif isinstance(a, crab.Crab) and top_row - 1 >= 0:
                labels_at_row.setdefault(top_row - 1, []).append((x, f"{a.name} ({a.get_age()})"))

        lines = []
        line_to_board_row = []
        # Display row length matches board (each cell is 2 chars: char + space)
        row_len = 2 * aq_width - 1
        for row_idx in range(self.aqua_height):
            if row_idx in labels_at_row:
                # Label line: same length and borders as board row so edges don't disappear
                label_chars = [" "] * row_len
                for (x, text) in labels_at_row[row_idx]:
                    start = 2 * x
                    for i, c in enumerate(text):
                        if start + i < row_len:
                            label_chars[start + i] = c
                label_chars[0], label_chars[-1] = "|", "|"
                lines.append("".join(label_chars))
                line_to_board_row.append(-1)
            lines.append(" ".join(board[row_idx]))
            line_to_board_row.append(row_idx)
        return lines, line_to_board_row

    def print_board(self):
        """Print the updated board on screen (hunger above each animal, name+age below)."""
        lines, _ = self.get_display_lines()
        for line in lines:
            print(line)

    def get_board(self):
        return self.board

    def get_all_animal(self):
        """Return the list of all animals in the aquarium."""
        return self.anim

    def _crab_row(self, row_from_top: int, crab_height: int) -> int:
        """Board row index for a crab line (0 = top of crab)."""
        return config.crab_row_index(self.aqua_height, crab_height, row_from_top)

    def is_collision(self, a: animal.Animal) -> bool:
        """Return True if the next step of the crab would cause a collision."""
        x, y = a.get_position()
        a_dir = a.get_directionH()
        aq_height = self.aqua_height
        board = self.get_board()
        zone_top = config.crab_zone_top_row(aq_height)
        crabs = [c for c in self.get_all_animal() if isinstance(c, crab.Crab)]
        for crab_2 in crabs:
            if (a_dir == config.DIR_RIGHT and crab_2.x == x + a.width) or \
                    (a_dir == config.DIR_LEFT and crab_2.x + crab_2.width == x):
                self.delete_animal_from_board(crab_2)
                crab_2.set_directionH(config.DIR_RIGHT) if crab_2.get_directionH() == config.DIR_LEFT else \
                    crab_2.set_directionH(config.DIR_LEFT) if crab_2.get_directionH() == config.DIR_RIGHT else None
                self.print_animal_on_board(crab_2)

                self.delete_animal_from_board(a)
                try:
                    if (board[zone_top][x - 1] not in ['|', '*'] and
                            board[zone_top + 1][x - 1] not in ['|', '*']):
                        a.set_x(x - 1)
                    elif (board[zone_top][x + a.width + 1] not in ['|', '*'] and
                          board[zone_top + 1][x + a.width + 1] not in ['|', '*']):
                        a.set_x(x + 1)
                except IndexError:
                    pass
                a.set_directionH(config.DIR_LEFT) if a_dir == config.DIR_RIGHT else \
                    a.set_directionH(config.DIR_RIGHT) if a_dir == config.DIR_LEFT else None
                self.print_animal_on_board(a)
                return True
        return False

    def print_animal_on_board(self, a: animal.Animal):
        k = a.get_animal()
        x, y = a.get_position()
        an_height, an_width = a.get_size()
        aq_height, aq_width = self.aqua_height, self.aqua_width
        board = self.get_board()
        if isinstance(a, fish.Fish):
            if (aq_width - x) < an_width + 1:
                a.set_x(aq_width - an_width - 1)
            for i in range(an_height):
                board[y + i][x:x + an_width] = k[i]
        elif isinstance(a, crab.Crab):
            if (aq_width - x) < an_width + 1:
                a.set_x(aq_width - an_width - 1)
            for i in range(an_height):
                board[self._crab_row(i, an_height)][x:x + an_width] = k[i]

    def delete_animal_from_board(self, a: animal.Animal):
        x, y = a.get_position()
        an_height, an_width = a.get_size()
        board = self.get_board()
        aq_height = self.aqua_height
        if isinstance(a, fish.Fish):
            for h in range(an_height):
                row_idx = y + h
                # Restore waterline so '~' is not permanently erased when fish touches surface
                fill = '~' if row_idx == config.WATERLINE_ROW else ' '
                board[row_idx][x:x + an_width] = fill * an_width
        else:
            for i in range(an_height):
                row_idx = self._crab_row(i, an_height)
                fill = '~' if row_idx == config.WATERLINE_ROW else ' '
                board[row_idx][x:x + an_width] = fill * an_width

    def add_animal(self, name, age, x, y, directionH, directionV, animaltype):
        if animaltype in ('sc', 'mo'):
            return self.add_fish(name, age, x, y, directionH, directionV, animaltype)
        if animaltype in ('oc', 'sh'):
            return self.add_crab(name, age, x, y, directionH, animaltype)
        return False

    def add_fish(self, name, age, x, y, directionH, directionV, fishtype):
        """Add a fish to the aquarium."""
        aq_height, aq_width = self.aqua_height, self.aqua_width
        if (aq_width - x) < config.MAX_FISH_WIDTH + 1:
            x = aq_width - config.MAX_FISH_WIDTH - 1

        fish_bottom = config.fish_lowest_y(aq_height)
        if fishtype == 'sc':
            if (aq_height - config.MAX_ANIMAL_HEIGHT - 1) <= y:
                y = fish_bottom - config.SCALAR_HEIGHT
            new_fish = scalar.Scalar(name, age, x, y, directionH, directionV)
            check_w, check_h = config.SCALAR_WIDTH, config.SCALAR_HEIGHT
        elif fishtype == 'mo':
            if (aq_height - config.MAX_ANIMAL_HEIGHT) <= y:
                y = fish_bottom - config.MOLY_HEIGHT
            new_fish = moly.Moly(name, age, x, y, directionH, directionV)
            check_w, check_h = config.MOLY_WIDTH, config.MOLY_HEIGHT
        else:
            return False

        if not self.check_if_free(x, y, width=check_w, height=check_h):
            print("The place is not available! Please try again later. ")
            return False

        self.anim.append(new_fish)
        self.print_animal_on_board(new_fish)
        return True

    def add_crab(self, name, age, x, y, directionH, crabtype):
        """Add a crab to the aquarium."""
        if (self.aqua_width - x) < config.MAX_CRAB_WIDTH + 1:
            x = self.aqua_width - config.MAX_CRAB_WIDTH - 1
        y = self.aqua_height - config.MAX_CRAB_HEIGHT

        check_w = config.SHRIMP_WIDTH if crabtype == 'sh' else config.OCYPODE_WIDTH
        check_h = config.SHRIMP_HEIGHT if crabtype == 'sh' else config.OCYPODE_HEIGHT
        if not self.check_if_free(x, y, width=check_w, height=check_h):
            print("The place is not available! Please try again later. ")
            return False

        if crabtype == 'sh':
            new_crab = shrimp.Shrimp(name, age, x, y, directionH)
        elif crabtype == 'oc':
            new_crab = ocypode.Ocypode(name, age, x, y, directionH)
        else:
            return False
        self.anim.append(new_crab)
        self.print_animal_on_board(new_crab)
        return True

    def check_if_free(
        self,
        x: int,
        y: int,
        width: int | None = None,
        height: int | None = None,
    ) -> bool:
        """Check if the area at (x, y) with given width/height is free. Uses full animal bounds if not specified."""
        w = width if width is not None else config.MAX_ANIMAL_WIDTH
        h = height if height is not None else config.MAX_ANIMAL_HEIGHT
        try:
            for t in range(h):
                row_idx = y + t
                if row_idx < 0 or row_idx >= self.aqua_height:
                    continue
                row = self.board[row_idx]
                x0, x1 = max(0, x), min(self.aqua_width, x + w)
                if '*' in row[x0:x1]:
                    return False
        except IndexError:
            return False
        return True

    def left(self, a: animal.Animal):
        x, y = a.get_position()
        if self.board[y][x - 1] == '|':
            self.delete_animal_from_board(a)
            a.set_directionH(config.DIR_RIGHT)
            return self.print_animal_on_board(a)

        if isinstance(a, crab.Crab):
            if self.is_collision(a):
                return None

        self.delete_animal_from_board(a)
        a.left()
        self.print_animal_on_board(a)

    def right(self, a: animal.Animal):
        x, y = a.get_position()
        if (isinstance(a, crab.Crab) and self.board[y][x + a.width] == '|') or \
                (isinstance(a, fish.Fish) and self.board[y][x + a.width] == '|'):
            self.delete_animal_from_board(a)
            a.set_directionH(config.DIR_LEFT)
            return self.print_animal_on_board(a)

        if isinstance(a, crab.Crab):
            if self.is_collision(a):
                return None

        self.delete_animal_from_board(a)
        a.right()
        self.print_animal_on_board(a)

    def up(self, a: animal.Animal):
        x, y = a.get_position()
        if y == config.WATERLINE:
            self.delete_animal_from_board(a)
            a.set_directionV(config.DIR_DOWN)
            return self.print_animal_on_board(a)
        self.delete_animal_from_board(a)
        a.up()
        self.print_animal_on_board(a)

    def down(self, a: animal.Animal):
        x, y = a.get_position()
        bottom = config.fish_lowest_y(self.aqua_height)
        if y + a.height >= bottom:
            a.set_directionV(config.DIR_UP)
            self.delete_animal_from_board(a)
            self.print_animal_on_board(a)
            return None
        self.delete_animal_from_board(a)
        a.down()
        self.print_animal_on_board(a)

    def next_turn(self):
        """Advance the simulation by one step."""
        for a in self.anim[:]:
            if self.turn % config.TURNS_PER_FOOD_DECREMENT == 0:
                a.dec_food()
                if self.turn % config.TURNS_PER_AGE_INCREMENT == 0:
                    old_age = a.get_age()
                    a.inc_age()
                    if a.get_alive() and a.get_age() != old_age:
                        print(f"  >> {a.name} is now {a.get_age()} years old!")

                if not a.get_alive():
                    self.delete_animal_from_board(a)
                    self.anim.remove(a)
                    continue

            try:
                if a.get_directionV() == config.DIR_DOWN:
                    self.down(a)
                else:
                    self.up(a)
            except AttributeError:
                pass

            if a.get_directionH() == config.DIR_RIGHT:
                self.right(a)
                if a.get_directionH() == config.DIR_LEFT:
                    continue
            else:
                self.left(a)

        for a in self.anim:
            self.delete_animal_from_board(a)
            self.print_animal_on_board(a)

        self.turn += 1

    def print_all(self):
        """Print all animals in the aquarium."""
        for a in self.anim:
            print(a)

    def reset(self):
        """Remove all animals and redraw an empty tank."""
        self.anim.clear()
        self.build_tank()

    def feed_all(self):
        """Feed all animals in the aquarium."""
        for a in self.get_all_animal():
            a.add_food(config.FEED_AMOUNT)

    def several_steps(self):
        """Advance the simulation by a user-specified number of steps."""
        valid_input = False
        while not valid_input:
            num_of_steps = input('How many step do you want to take?')
            num_of_steps = valid_num_check(num_of_steps)
            if not num_of_steps:
                continue
            valid_input = True
        for _ in range(num_of_steps):
            self.next_turn()
