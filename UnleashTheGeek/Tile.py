class Tile:
    def __init__(self, x: int, y: int, scrap_amount: int, owner: int, units: int, recycler: bool, can_build: bool, can_spawn: bool, in_range_of_recycler: bool):
        self.x = x
        self.y = y
        self.scrap_amount = scrap_amount
        self.owner = owner
        self.units = units
        self.recycler = recycler
        self.can_build = can_build
        self.can_spawn = can_spawn
        self.in_range_of_recycler = in_range_of_recycler
    def get_coordinates(self):
        return [self.x, self.y]
    def is_grass(self):
        return self.scrap_amount < 0
    def is_recycler(self):
        return self.recycler == 1
    def is_neutral(self):
        return self.owner == -1
    def is_opponent(self):
        return self.owner == 0
    def is_mine(self):
        return self.owner == 1
    def has_units(self):
        return self.units > 0
    def can_build(self):
        return self.can_build == 1
    def can_spawn(self):
        return self.can_spawn == 1