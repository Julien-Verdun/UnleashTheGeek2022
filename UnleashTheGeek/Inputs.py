class Inputs:
    def __init__(self, height, width, me, opp):
        self.height = height
        self.width = width
        self.me = me
        self.opp = opp
        self.my_matter = 0
        self.opp_matter = 0
        self.tiles = []
        self.my_units = []
        self.opp_units = []
        self.my_recyclers = []
        self.opp_recyclers = []
        self.opp_tiles = []
        self.my_tiles = []
        self.neutral_tiles = []
        self.other_tiles = []
        self.targeted_tiles = []

    def readInput(self):

        self.my_matter, self.opp_matter = [int(i) for i in input().split()]
        # Game logic (Game class)
        # Outputs print (OutputPrint class)
        for y in range(self.height):
            for x in range(self.width):
                # owner: 1 = me, 0 = foe, -1 = neutral
                # recycler, can_build, can_spawn, in_range_of_recycler: 1 = True, 0 = False
                scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [
                    int(k) for k in input().split()]
                tile = Tile(x, y, scrap_amount, owner, units, recycler == 1,
                            can_build == 1, can_spawn == 1, in_range_of_recycler == 1)

                self.tiles.append(tile)

                if tile.owner == self.me:
                    self.my_tiles.append(tile)
                    if tile.units > 0:
                        self.my_units.append(tile)
                    elif tile.recycler:
                        self.my_recyclers.append(tile)
                elif tile.owner == self.opp:
                    self.opp_tiles.append(tile)
                    if tile.units > 0:
                        self.opp_units.append(tile)
                    elif tile.recycler:
                        self.opp_recyclers.append(tile)
                else:
                    self.other_tiles.append(tile)
                    if tile.scrap_amount > 0:
                        self.neutral_tiles.append(tile)
        self.targeted_tiles = self.neutral_tiles + self.opp_tiles
