from . import config, crab


class Ocypode(crab.Crab):
    def __init__(self, name, age, x, y, directionH):
        super().__init__(name, age, x, y, directionH)
        self.width = config.OCYPODE_WIDTH
        self.height = config.OCYPODE_HEIGHT

    def get_animal(self):
        ocypode = [
            ' *   * ',
            '  ***  ',
            '*******',
            '*     *'
        ]
        return ocypode
