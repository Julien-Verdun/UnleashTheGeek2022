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
            tiles = []
            for x in range(self.width):
                # owner: 1 = me, 0 = foe, -1 = neutral
                # recycler, can_build, can_spawn, in_range_of_recycler: 1 = True, 0 = False
                scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [
                    int(k) for k in input().split()]
                tile = Tile(x, y, scrap_amount, owner, units, recycler == 1,
                            can_build == 1, can_spawn == 1, in_range_of_recycler == 1)

                tiles.append(tile)

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
            self.tiles.append(tiles)
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
    def __init__(self, height, width):
        self.turn = 0
        self.inputs = None
        self.height = height
        self.width = width
        self.interval_recycler = 3

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
            return Coordinate( int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x*tile.units, self.inputs.opp_units) )/sum(list(map(lambda tile: tile.units, self.inputs.opp_units))) ), int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x, self.inputs.opp_units) )/sum(list(map(lambda tile: tile.units, self.inputs.opp_units)))) )
        else:
            return None

    def get_closest_tile_from_opponent_tile(self, opponent_tile):
        return self.get_closest_tile(opponent_tile, self.inputs.my_tiles)

    def number_grass_free_neighbour_tiles(self, tile):
        if tile.x > 0 and tile.x < self.width-1 and tile.y > 0 and tile.y < self.height-1:     
            return tile.scrap_amount  + self.inputs.tiles[tile.y-1][tile.x].scrap_amount + self.inputs.tiles[tile.y+1][tile.x].scrap_amount + self.inputs.tiles[tile.y][tile.x-1].scrap_amount + self.inputs.tiles[tile.y][tile.x+1].scrap_amount
        return 0


    def is_tile_near_recycler(self,tile):
        for recycler in self.inputs.my_recyclers:
            if (recycler.x == tile.x and abs(recycler.y-tile.y)==2) or (recycler.y == tile.y and abs(recycler.x-tile.x)==2) or (abs(recycler.x-tile.x)==1 and abs(recycler.y-tile.y)==1):
                return True
        return False

    def get_best_recycler_tile(self):
        # TO-DO : Check that a recycler is not too close 
        list_eligible_tiles = list(filter(lambda tile: tile.can_build == 1 and tile.units == 0 and not self.is_tile_near_recycler(tile), self.inputs.my_tiles))
        list_scrap_amounts = list(map(lambda tile : self.number_grass_free_neighbour_tiles(tile), list_eligible_tiles ))
        
        if len(list_scrap_amounts) > 0:
            best_recycler_location_index = np.argmax(list_scrap_amounts)
            return list_eligible_tiles[best_recycler_location_index]
        return None

    def play(self):
        actions = []
        
        if self.turn % self.interval_recycler != 0 :
            opponent_center = self.get_opponent_center()
            if opponent_center != None:
                closest_tile_from_opponent_tile = self.get_closest_tile_from_opponent_tile(opponent_center)
                if closest_tile_from_opponent_tile != None and closest_tile_from_opponent_tile.can_spawn:
                    if self.inputs.my_matter >= 10:
                                amount = self.inputs.my_matter // 10  
                                if amount > 0:
                                    actions.append('SPAWN {} {} {}'.format(
                                        amount, closest_tile_from_opponent_tile.x, closest_tile_from_opponent_tile.y))
        else:
            if self.inputs.my_matter >= 10:
                tile = self.get_best_recycler_tile()
                if tile != None:
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
        self.turn += 1
        return actions



game = Game(HEIGHT, WIDTH)

while True:
    inputs = Inputs(HEIGHT, WIDTH, ME, OPP)
    inputs.readInput()
    game.inputs = inputs
    actions = game.play()

    print(actions, file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')



