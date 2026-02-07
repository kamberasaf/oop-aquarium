from . import config, fish


class Moly(fish.Fish):
    def __init__(self, name, age, x, y, directionH, directionV):
        super().__init__(name, age, x, y, directionH, directionV)
        self.width = config.MOLY_WIDTH
        self.height = config.MOLY_HEIGHT

    def get_animal(self):
        moly = [
            '*   *** ',
            '********',
            '*   *** '
        ]
        if self.directionH == config.DIR_LEFT:
            moly = [i[::-1] for i in moly]
        return moly
