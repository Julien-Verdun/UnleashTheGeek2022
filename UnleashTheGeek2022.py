import math
import time
import numpy as np
from functools import reduce
import sys
import random 

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
        self.can_build_bool = can_build
        self.can_spawn_bool = can_spawn
        self.in_range_of_recycler = in_range_of_recycler
    def get_coordinates(self):
        return [self.x, self.y]
    def is_grass(self):
        return self.scrap_amount <= 0
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
        return self.can_build_bool == 1
    def can_spawn(self):
        return self.can_spawn_bool == 1



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
        # self.compute_diffusion_matrix()

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

        # print(diffusion_matrix, file=sys.stderr, flush=True)
        return diffusion_matrix



class Game:
    def __init__(self, height, width):
        self.turn = 0
        self.inputs = None
        self.height = height
        self.width = width
        self.interval_recycler = 2
        self.ratio_scouters = 1
        self.height_threshold = 8
        self.should_build_recycler = True
        self.number_turn_for_strategy = 5

    def distance_tiles(self, tileA, tileB):
        return self.distance(tileA.x, tileA.y, tileB.x, tileB.y) 

    def distance(self, xA, yA, xB, yB):
        return math.sqrt((xA - xB)**2 + (yA - yB)**2)
    
    def update_interval_recycler(self):
        if self.height >= self.height_threshold:
            self.number_turn_for_strategy = 10
            if self.turn < 5:
                self.interval_recycler = 2
            elif self.turn < 20:
                self.interval_recycler = 1
            elif self.turn < 40:
                self.interval_recycler = 2
            elif self.turn >= 50:
                self.interval_recycler = 1000

            if self.turn < 25:
              self.ratio_scouters = 1
            elif self.turn < 40:
                self.ratio_scouters = 0.8
            else:
                self.ratio_scouters = 0.6
        else:
            self.number_turn_for_strategy = 5
            if self.turn < 6:
                self.interval_recycler = 2
            elif self.turn < 12:
                self.interval_recycler = 1
            elif self.turn < 20:
                self.interval_recycler = 5
            elif self.turn < 40:
                self.interval_recycler = 10
            elif self.turn >= 40:
                self.interval_recycler = 1000

            if self.turn < 15:
                self.ratio_scouters = 1
            elif self.turn < 30:
                self.ratio_scouters = 0.8
            else:
                self.ratio_scouters = 0.6


    def get_extreme_tiles(self,tile, list_tiles, ratio=0.2):
        ordered_tiles = list_tiles
        if len(list_tiles) > 0:
            ordered_tiles.sort(reverse = True,key=lambda tile_to_sort : self.distance_tiles(tile_to_sort, tile))
            return ordered_tiles[:int(len(ordered_tiles)*ratio)], ordered_tiles[int(len(ordered_tiles)*ratio):]
        else:
            return [],[]

    def get_extreme_tile(self,tile, list_tiles, aggregator="min"):
        distances = list(map(lambda targeted_tile : self.distance_tiles(targeted_tile, tile) ,list_tiles))
        if len(distances) > 0:
            if aggregator == "min":
                tile_index = np.argmin(distances)
            else:
                tile_index = np.argmax(distances)
            return list_tiles[tile_index]
        return None 

    def find_closest_targeted_tiles(self, current_tile, should_target_ennemy, number_output_tiles = 1, opponent_tiles=None):
        if should_target_ennemy:
            if current_tile.units < 2:  
                return [self.get_extreme_tile(current_tile, opponent_tiles)]
            else:
                number_output_tiles = min(number_output_tiles, current_tile.units)
                farest_tiles, _ = self.get_extreme_tiles(current_tile, opponent_tiles, 1)
                farest_tiles.reverse()
                # list distances ordered by asc order 
                if len(farest_tiles) > number_output_tiles:
                    return farest_tiles[:number_output_tiles] 
                else:
                    return farest_tiles
        else:
            if current_tile.units < 2:  
                return [self.get_extreme_tile(current_tile,  self.inputs.targeted_tiles)]
            else:
                number_output_tiles = min(number_output_tiles, current_tile.units)
                farest_tiles, _ = self.get_extreme_tiles(current_tile, opponent_tiles, 1)
                farest_tiles.reverse()
                # list distances ordered by asc order 
                if len(farest_tiles) > number_output_tiles:
                    return farest_tiles[:number_output_tiles] 
                else:
                    return farest_tiles
        # return [self.get_extreme_tile(current_tile, self.inputs.targeted_tiles)]

    def get_opponent_center(self):
        if len(self.inputs.opp_units) > 0:
            total_nb_of_opponent_units = sum(list(map(lambda tile: tile.units, self.inputs.opp_units)))
            return Coordinate(int(sum(list(map(lambda tile : tile.x*tile.units, self.inputs.opp_units)))/total_nb_of_opponent_units),int(sum(list(map(lambda tile : tile.y*tile.units, self.inputs.opp_units)))/total_nb_of_opponent_units))
        else:
            return None

    def get_extreme_tiles_from_opponent_center(self, ratio):
        opponent_center = self.get_opponent_center()
        return self.get_extreme_tiles(opponent_center, self.inputs.my_units, ratio)

    def get_closest_tiles_from_opponent_tile(self, opponent_tile):
        farest_tiles, _  = self.get_extreme_tiles(opponent_tile, self.inputs.my_tiles, 1)
        farest_tiles.reverse()
        return farest_tiles

    def total_scrap_amount_of_adjacent_tiles(self, tile):
        if tile.x > 0 and tile.x < self.width-1 and tile.y > 0 and tile.y < self.height-1:     
            return tile.scrap_amount  + self.inputs.tiles[tile.y-1][tile.x].scrap_amount + self.inputs.tiles[tile.y+1][tile.x].scrap_amount + self.inputs.tiles[tile.y][tile.x-1].scrap_amount + self.inputs.tiles[tile.y][tile.x+1].scrap_amount
        return 0

    def is_tile_near_recycler(self,tile):
        for recycler in self.inputs.my_recyclers:
            if (recycler.x == tile.x and abs(recycler.y-tile.y)<=2) or (recycler.y == tile.y and abs(recycler.x-tile.x)<=2) or (abs(recycler.x-tile.x)==1 and abs(recycler.y-tile.y)==1):
                return True
        return False

    def get_best_recycler_tile(self, logic="closer_to_opp"):
        if logic == "best_amount":
            list_eligible_tiles = list(filter(lambda tile: tile.can_build() and not tile.has_units() and (not self.is_tile_near_recycler(tile)), self.inputs.my_tiles))
            if len(list_eligible_tiles) > 0:
                list_scrap_amounts = list(map(lambda tile : self.total_scrap_amount_of_adjacent_tiles(tile), list_eligible_tiles ))
                best_recycler_location_index = np.argmax(list_scrap_amounts)
                return list_eligible_tiles[best_recycler_location_index]
        elif logic == "closer_to_opp":
            opponent_center = self.get_opponent_center()
            closest_tile_from_opponent_tiles = self.get_closest_tiles_from_opponent_tile(opponent_center)
            list_eligible_tiles = list(filter(lambda tile: tile.can_build() and not tile.has_units() and (not self.is_tile_near_recycler(tile)), closest_tile_from_opponent_tiles))
            if len(list_eligible_tiles) > 0:
                return list_eligible_tiles[0]
        return None


    def get_action_to_move_tile_to_closest(self, my_tile, closest_targeted_tiles):
        tile_actions = []
        for idx, closest_target in enumerate(closest_targeted_tiles):
            if closest_target != None:
                target = Coordinate(closest_target.x, closest_target.y)
            else :
                target = Coordinate(my_tile.x+[-1, 1][random.randint(0,1)],
                                my_tile.y+[-1, 1][random.randint(0,1)])
            if target:
                amount = my_tile.units // len(closest_targeted_tiles)  # TODO: pick amount of units to move
                if idx == 0:
                    amount += my_tile.units % len(closest_targeted_tiles)
                tile_actions.append('MOVE {} {} {} {} {}'.format(
                    amount, my_tile.x, my_tile.y, target.x, target.y))
        return tile_actions

    def play(self, t0):
        actions = []
        if self.should_build_recycler == True and self.turn % self.interval_recycler == 0 :
            if self.inputs.my_matter >= 10:
                if self.turn <= self.number_turn_for_strategy:
                    tile = self.get_best_recycler_tile("best_amount")
                else:
                    tile = self.get_best_recycler_tile("closer_to_opp")
                if tile != None:
                    actions.append('BUILD {} {}'.format(tile.x, tile.y))
                    self.inputs.my_matter -= 10
        if self.inputs.my_matter >= 10:
            opponent_center = self.get_opponent_center()
            if opponent_center != None:
                closest_tile_from_opponent_tiles = self.get_closest_tiles_from_opponent_tile(opponent_center)
                if len(closest_tile_from_opponent_tiles) > 0:
                    closest_tile_from_opponent_tiles = list(filter(lambda closest_tile_from_opponent_tile: closest_tile_from_opponent_tile != None and closest_tile_from_opponent_tile.can_spawn(), closest_tile_from_opponent_tiles))
                    # ! list
                    amount = self.inputs.my_matter // 10  
                    if amount > 0 and len(closest_tile_from_opponent_tiles) > 0:
                        spawn_tiles = closest_tile_from_opponent_tiles[:min(amount,len(closest_tile_from_opponent_tiles))]
                        for idx,closest_tile in enumerate(spawn_tiles):
                            if idx == 0:
                                actions.append('SPAWN {} {} {}'.format(amount // len(spawn_tiles) + amount % len(spawn_tiles), closest_tile.x, closest_tile.y))
                            else:
                                actions.append('SPAWN {} {} {}'.format(amount // len(spawn_tiles), closest_tile.x, closest_tile.y))

        farest_tiles, closest_tiles = self.get_extreme_tiles_from_opponent_center(self.ratio_scouters)
        
        targeted_tiles = self.inputs.targeted_tiles
        for tile in farest_tiles:
            if len(targeted_tiles) ==0:
                targeted_tiles = self.inputs.targeted_tiles
            closest_targeted_tiles = self.find_closest_targeted_tiles(
                tile, False, tile.units, targeted_tiles)
            targeted_tiles = list(filter(lambda target: target.get_coordinates() not in list(map(lambda closest_tile: closest_tile.get_coordinates(), closest_targeted_tiles)) , targeted_tiles))
            actions += self.get_action_to_move_tile_to_closest(tile, closest_targeted_tiles)

        # opponent_tiles = self.inputs.opp_tiles
        opponent_tiles = self.inputs.opp_units
        for tile in closest_tiles:
            if len(opponent_tiles)==0:
                opponent_tiles = self.inputs.opp_units
                # opponent_tiles = self.inputs.opp_tiles
            closest_targeted_tiles = self.find_closest_targeted_tiles(
                tile, True, tile.units, opponent_tiles) #  math.ceil(tile.units / 2)
            opponent_tiles = list(filter(lambda opp: opp.get_coordinates() not in list(map(lambda closest_tile: closest_tile.get_coordinates(), closest_targeted_tiles)) , opponent_tiles))
            actions += self.get_action_to_move_tile_to_closest(tile, closest_targeted_tiles)

        self.turn += 1
        self.update_interval_recycler()
        return actions




game = Game(HEIGHT, WIDTH)


while True:
    t0 = time.time()
    inputs = Inputs(HEIGHT, WIDTH)
    inputs.readInput()
    game.inputs = inputs
    number_tiles = [5]
    # actions = game.play(t0)
    # print(actions, file=sys.stderr, flush=True)
    # print(time.time()-t0, file=sys.stderr, flush=True)
    try:
        actions = game.play(t0)
        number_tiles.append(len(game.inputs.my_tiles))
        if len(number_tiles) > 10 and abs(number_tiles[-1] - number_tiles[-2]) <= 5:
            game.should_build_recycler = False
        print(actions, file=sys.stderr, flush=True)
    except:
        actions = ["WAIT"]
        print("Something went wrong when running the gameplay !", file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')


