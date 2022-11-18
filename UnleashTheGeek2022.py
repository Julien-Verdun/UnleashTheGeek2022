import math
import random 
from functools import reduce
import numpy as np
import sys

WIDTH, HEIGHT = [int(i) for i in input().split()]



class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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



class Inputs:
    def __init__(self, height, width):
        self.height = height
        self.width = width
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
        self.grass_tiles = []
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

                if tile.is_mine():
                    if tile.has_units():
                        self.my_units.append(tile)
                    if tile.is_recycler():
                        self.my_recyclers.append(tile)
                    else:
                        self.my_tiles.append(tile)
                elif tile.is_opponent():
                    if tile.has_units():
                        self.opp_units.append(tile)
                    if tile.is_recycler():
                        self.opp_recyclers.append(tile)
                    else:
                        self.opp_tiles.append(tile)
                else:
                    if not tile.is_grass():
                        self.neutral_tiles.append(tile)
                    else :
                        self.grass_tiles.append(tile)
            self.tiles.append(tiles)
            self.targeted_tiles = self.neutral_tiles + self.opp_tiles
            # list(filter(lambda opp_tile: opp_tile.get_coordinates() not in list(map(lambda recycler : recycler.get_coordinates() ,self.opp_recyclers)) ,self.opp_tiles))
        self.compute_diffusion_matrix()

    def compute_diffusion_matrix(self):
        diffusion_matrix = np.zeros((self.height, self.width))
        size_local_matrix = 5
        max_local_matrix = 100
     
        local_diffusion_matrix = np.zeros((size_local_matrix,size_local_matrix))
        for i in range(size_local_matrix//2+1):
            for j in range(size_local_matrix//2+1):
                local_diffusion_matrix[i,j]= int(max_local_matrix / (abs(2*(size_local_matrix//2)-i-j) + 1))
        local_diffusion_matrix[:size_local_matrix//2+1,size_local_matrix//2:] = np.flip(local_diffusion_matrix[:size_local_matrix//2+1,:size_local_matrix//2+1],axis=1)
        local_diffusion_matrix[size_local_matrix//2:,:size_local_matrix//2+1] = np.flip(local_diffusion_matrix[:size_local_matrix//2+1,:size_local_matrix//2+1],axis=0)
        local_diffusion_matrix[size_local_matrix//2:,size_local_matrix//2:] = np.flip(np.flip(local_diffusion_matrix[:size_local_matrix//2+1,:size_local_matrix//2+1],axis=1),axis=0)
        # print(local_diffusion_matrix, file=sys.stderr, flush=True)

        for tile in self.opp_tiles:
            # print(str(self.height) + " " + str(self.width), file=sys.stderr, flush=True)
            # print(' - '.join(list(map(lambda x: str(x), [tile.y-size_local_matrix//2,tile.y+size_local_matrix//2+1, tile.x-size_local_matrix//2,tile.x+size_local_matrix//2+1]))), file=sys.stderr, flush=True)
            
            
            # if tile.y - size_local_matrix//2 >= 0 and tile.y + size_local_matrix//2 < self.height and tile.x - size_local_matrix//2 >= 0 and tile.x + size_local_matrix//2 < self.width:
            #     diffusion_matrix[tile.y-size_local_matrix//2:tile.y+size_local_matrix//2+1, tile.x-size_local_matrix//2:tile.x+size_local_matrix//2+1] += local_diffusion_matrix
            # else:
            #     pass


            if tile.y - size_local_matrix > 0  and tile.y + size_local_matrix < self.height-1 and tile.x - size_local_matrix > 0 and tile.x + size_local_matrix < self.width-1:
                diffusion_matrix[math.max(0,tile.y-size_local_matrix//2):math.min(tile.y+size_local_matrix//2+1, self.height), math.max(0,tile.x-size_local_matrix//2):math.min(tile.x+size_local_matrix//2+1, self.width)] += local_diffusion_matrix[math.max(0,-(tile.y-size_local_matrix//2)):size_local_matrix + math.min(0, self.height-(tile.y+size_local_matrix//2+1)),math.max(0,-(tile.x-size_local_matrix//2) ):size_local_matrix + math.min(0, self.width - (tile.x+size_local_matrix//2+1) )]
                # TO-DO: add logic to add sub matrix 
              

                 
        for tile in self.grass_tiles:
            diffusion_matrix[tile.y,tile.x] = -1

        print(diffusion_matrix, file=sys.stderr, flush=True)
        return diffusion_matrix



class Game:
    def __init__(self, height, width):
        self.turn = 0
        self.inputs = None
        self.height = height
        self.width = width
        self.interval_recycler = 2
        self.ratio_scouters = 0.2

    def distance_tiles(self, tileA, tileB):
        return self.distance(tileA.x, tileA.y, tileB.x, tileB.y) 

    def distance(self, xA, yA, xB, yB):
        return math.sqrt((xA - xB)**2 + (yA - yB)**2)
    
    def update_interval_recycler(self):
        if self.turn < 10:
            self.interval_recycler = 2
        elif self.turn < 20:
            self.interval_recycler = 3
        else:
            self.interval_recycler = 4

    def get_extreme_tiles(self,tile, list_tiles, ratio=0.2):
        ordered_tiles = list_tiles.sort(reverse = True,key=lambda sorted_tile : self.distance_tiles(sorted_tile, tile))
        return ordered_tiles[:int(len(ordered_tiles)*ratio)], ordered_tiles[int(len(ordered_tiles)*ratio):]

    def get_extreme_tile(self,tile, list_tiles, aggregator="min"):
        distances = list(map(lambda targeted_tile : self.distance_tiles(targeted_tile, tile) ,list_tiles))
        if len(distances) > 0:
            if aggregator == "min":
                closest_tile_index = np.argmin(distances)
            else:
                closest_tile_index = np.argmax(distances)
            return list_tiles[closest_tile_index]
        return None 

    def find_closest_targeted_tile(self, current_tile, should_target_ennemy):
        # TODO : optimize to get more diversity in the way the robot are looking for targeted tiles
        if should_target_ennemy:
            return self.get_extreme_tile(current_tile, self.inputs.opp_tiles)
        return self.get_extreme_tile(current_tile, self.inputs.targeted_tiles)

    def get_opponent_center(self):
        if len(self.inputs.opp_units) > 0:
            return Coordinate( int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x*tile.units, self.inputs.opp_units) )/sum(list(map(lambda tile: tile.units, self.inputs.opp_units))) ), int(reduce(lambda xA, xB : xA + xB,map(lambda tile : tile.x, self.inputs.opp_units) )/sum(list(map(lambda tile: tile.units, self.inputs.opp_units)))) )
        else:
            return None

    def get_extreme_tiles_from_opponent_center(self, ratio):
        opponent_center = self.get_opponent_center()
        return self.get_extreme_tiles(opponent_center, self.inputs.my_units, ratio)


    def get_closest_tile_from_opponent_tile(self, opponent_tile):
        return self.get_extreme_tile(opponent_tile, self.inputs.my_tiles)

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
        list_eligible_tiles = list(filter(lambda tile: tile.can_build() and not tile.has_units() and (not self.is_tile_near_recycler(tile)), self.inputs.my_tiles))
        list_scrap_amounts = list(map(lambda tile : self.number_grass_free_neighbour_tiles(tile), list_eligible_tiles ))
        print(str(len(list_eligible_tiles))+"-"+str(len(self.inputs.my_tiles)), file=sys.stderr, flush=True)
        if len(list_scrap_amounts) > 0:
            best_recycler_location_index = np.argmax(list_scrap_amounts)
            return list_eligible_tiles[best_recycler_location_index]
        return None

    # def spread_my_units(self):
    #     # compute 80% units closest to ennemy center
    #     # send 20% farest one in the opposite direction
    #     # send the rest in direction of ennemy and in different tiles  
    #     opponent_center = self.get_opponent_center()
    #     distances_units_to_ennemy_center = list(map(lambda unit : self.distance(unt.x, unit.y, opponent_center.x, opponent_center.y) ,self.inputs.my_units))

    def get_action_to_move_tile_to_closest(self, tile, closest_targeted_tile):
        if closest_targeted_tile != None:
            target = Coordinate(closest_targeted_tile.x, closest_targeted_tile.y)
        else :
            target = Coordinate(tile.x+random.randint(0, 2)-1,
                            tile.y+random.randint(0, 2)-1)
        if target:
            amount = tile.units  # TODO: pick amount of units to move
            return ['MOVE {} {} {} {} {}'.format(
                amount, tile.x, tile.y, target.x, target.y)]
        return []

    def play(self):
        actions = []
        
        add_recycler = False 
        if self.turn % self.interval_recycler == 0 :
            if self.inputs.my_matter >= 10:
                tile = self.get_best_recycler_tile()
                if tile != None:
                    actions.append('BUILD {} {}'.format(tile.x, tile.y))
                    add_recycler = True
        if not add_recycler or (add_recycler and self.inputs.my_matter - 10 >= 10) :
            opponent_center = self.get_opponent_center()
            if opponent_center != None:
                closest_tile_from_opponent_tile = self.get_closest_tile_from_opponent_tile(opponent_center)
                if closest_tile_from_opponent_tile != None and closest_tile_from_opponent_tile.can_spawn():
                    amount = (self.inputs.my_matter-10) // 10  
                    if amount > 0:
                        actions.append('SPAWN {} {} {}'.format(
                            amount, closest_tile_from_opponent_tile.x, closest_tile_from_opponent_tile.y))


       
        farest_tiles, closest_tiles = self.get_extreme_tiles_from_opponent_center(self.ratio_scouters)

        for tile in farest_tiles:
            closest_targeted_tile = self.find_closest_targeted_tile(
                tile, False)
            actions += self.get_action_to_move_tile_to_closest(tile, closest_targeted_tile)

        for tile in closest_tiles:
            closest_targeted_tile = self.find_closest_targeted_tile(
                tile, True)
            actions += self.get_action_to_move_tile_to_closest(tile, closest_targeted_tile)


        # Take the farest tile to farm neutral tiles
        # farest_tile = self.get_farest_tile_from_opponent_tiles(
        #     self.inputs.my_units)
        # for tile in self.inputs.my_units:
        #     if tile.get_coordinates() in [farest_tile.get_coordinates() for farest_tile in farest_tiles]:
        #         closest_targeted_tile = self.find_closest_targeted_tile(
        #         tile, False)
        #     else:
        #         closest_targeted_tile = self.find_closest_targeted_tile(
        #         tile, True)

        #     if closest_targeted_tile != None:
        #         target = Coordinate(closest_targeted_tile.x, closest_targeted_tile.y)
        #     else :
        #         target = Coordinate(tile.x+random.randint(0, 2)-1,
        #                         tile.y+random.randint(0, 2)-1)
        #     if target:
        #         amount = tile.units  # TODO: pick amount of units to move
        #         actions.append('MOVE {} {} {} {} {}'.format(
        #             amount, tile.x, tile.y, target.x, target.y))
        self.turn += 1
        self.update_interval_recycler()
        return actions



game = Game(HEIGHT, WIDTH)

while True:
    inputs = Inputs(HEIGHT, WIDTH)
    inputs.readInput()
    game.inputs = inputs
    try:
        actions = game.play()
        print(actions, file=sys.stderr, flush=True)
    except:
        actions = ["WAIT"]
        print("Something went wrong when running the gameplay !", file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')


