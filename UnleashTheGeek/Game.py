import random


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, inputs):
        self.inputs = inputs

    def play(self):
        actions = []

        for tile in self.inputs.my_tiles:
            if tile.can_spawn:
                amount = 0  # TODO: pick amount of robots to spawn here
                if amount > 0:
                    actions.append('SPAWN {} {} {}'.format(
                        amount, tile.x, tile.y))
            if tile.can_build:
                should_build = False  # TODO: pick whether to build recycler here
                if should_build:
                    actions.append('BUILD {} {}'.format(tile.x, tile.y))

        for tile in self.inputs.my_units:
            # TODO: pick a destination tile
            target = Coordinate(tile.x+random.randint(0, 2)-1,
                                tile.y+random.randint(0, 2)-1)
            # target = None
            if target:
                amount = 1  # TODO: pick amount of units to move
                actions.append('MOVE {} {} {} {} {}'.format(
                    amount, tile.x, tile.y, target.x, target.y))
        return actions
