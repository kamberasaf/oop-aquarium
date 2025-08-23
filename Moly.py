import Fish


class Moly(Fish.Fish):
    def __init__(self, name, age, x, y, directionH, directionV):
        super().__init__(name, age, x, y, directionH, directionV)
        self.width = 8
        self.height = 3

    def get_animal(self):
        moly = [
            '*   *** ',
            '********',
            '*   *** '
        ]

        if self.directionH == 0:
            moly = [i[::-1] for i in moly]  # a moly looking left.

        return moly