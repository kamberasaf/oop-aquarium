from . import config, fish


class Scalar(fish.Fish):
    def __init__(self, name, age, x, y, directionH, directionV):
        super().__init__(name, age, x, y, directionH, directionV)
        self.width = config.SCALAR_WIDTH
        self.height = config.SCALAR_HEIGHT

    def get_animal(self):
        scalar = [
            '******  ',
            '    *** ',
            '  ******',
            '    *** ',
            '******  '
        ]
        if self.directionH == config.DIR_LEFT:
            scalar = [i[::-1] for i in scalar]
        return scalar
