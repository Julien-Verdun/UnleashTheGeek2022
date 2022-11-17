import sys
import math
from dataclasses import dataclass

ME = 1
OPP = 0
NONE = -1

WIDTH, HEIGHT = [int(i) for i in input().split()]



@dataclass
class Tile:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool



class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y



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



import numpy as np
import math 
import random 
from functools import reduce

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self):
        self.inputs = None

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def get_closest_tile(self,tile, list_tiles):
        list_distances = list(map(lambda neutral_tile : self.distance(neutral_tile.x, neutral_tile.y, tile.x, tile.y) ,list_tiles))
        if len(list_distances) > 0:
            closest_tile_index = np.argmin(list_distances)
            return list_tiles[closest_tile_index]
        return None 

    def find_closest_neutral_tile(self, current_tile):
        # TODO : optimize to get more diversity in the way the robot are looking for targeted tiles
        return self.get_closest_tile(current_tile, self.inputs.targeted_tiles)  

    def get_opponent_center(self):
        if len(self.inputs.opp_units) > 0:
            return Coordinate( int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x, self.inputs.opp_units) )/len(self.inputs.opp_units)), int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x, self.inputs.opp_units) )/len(self.inputs.opp_units)) )
        else:
            return None

    def get_closest_tile_from_opponent_tile(self, opponent_tile):
        return self.get_closest_tile(opponent_tile, self.inputs.my_tiles)

    def play(self):
        actions = []
        
        opponent_center = self.get_opponent_center()
        if opponent_center != None:
            closest_tile_from_opponent_tile = self.get_closest_tile_from_opponent_tile(opponent_center)
            if closest_tile_from_opponent_tile != None:
                if self.inputs.my_matter >= 10:
                            amount = self.inputs.my_matter // 10  
                            if amount > 0:
                                actions.append('SPAWN {} {} {}'.format(
                                    amount, closest_tile_from_opponent_tile.x, closest_tile_from_opponent_tile.y))

        for tile in self.inputs.my_tiles:
            # if tile.can_spawn:
            #     # TODO: pick amount of robots to spawn here
            #     if self.inputs.my_matter >= 10:
            #         amount = self.inputs.my_matter // 10  
            #         if amount > 0:
            #             actions.append('SPAWN {} {} {}'.format(
            #                 amount, tile.x, tile.y))
            if tile.can_build:
                should_build = False  # TODO: pick whether to build recycler here
                if should_build:
                    actions.append('BUILD {} {}'.format(tile.x, tile.y))

        for tile in self.inputs.my_units:
            # TODO: pick a destination tile
            
            closest_neutral_tile = self.find_closest_neutral_tile(tile)
            if closest_neutral_tile != None:
                target = Coordinate(closest_neutral_tile.x, closest_neutral_tile.y)
            else :
                target = Coordinate(tile.x+random.randint(0, 2)-1,
                                tile.y+random.randint(0, 2)-1)
            # target = None
            if target:
                amount = tile.units  # TODO: pick amount of units to move
                actions.append('MOVE {} {} {} {} {}'.format(
                    amount, tile.x, tile.y, target.x, target.y))
        return actions



game = Game()

while True:
    inputs = Inputs(HEIGHT, WIDTH, ME, OPP)
    inputs.readInput()
    game.inputs = inputs
    actions = game.play()

    print(actions, file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')



