import Fish


class Scalar(Fish.Fish):
    def __init__(self, name, age, x, y, directionH, directionV):
        super().__init__(name, age, x, y, directionH, directionV)
        self.width = 8
        self.height = 5

    def get_animal(self):
        scalar = [
            '******  ',
            '    *** ',
            '  ******',
            '    *** ',
            '******  '
                ]

        if self.directionH == 0:  # if we need a scalar looking left.
            scalar = [i[::-1] for i in scalar]

        return scalar