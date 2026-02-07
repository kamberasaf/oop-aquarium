from . import config, crab


class Shrimp(crab.Crab):
    def __init__(self, name, age, x, y, directionH):
        super().__init__(name, age, x, y, directionH)
        self.width = config.SHRIMP_WIDTH
        self.height = config.SHRIMP_HEIGHT

    def get_animal(self):
        shrimp = [
            '    * *',
            '****** ',
            '  * *  '
        ]
        if self.directionH == config.DIR_LEFT:
            shrimp = [i[::-1] for i in shrimp]
        return shrimp
