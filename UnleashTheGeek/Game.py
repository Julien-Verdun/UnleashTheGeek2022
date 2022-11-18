import numpy as np
import math
import random 
from functools import reduce

class Game:
    def __init__(self, height, width):
        self.turn = 0
        self.inputs = None
        self.height = height
        self.width = width
        self.interval_recycler = 2
        self.ratio_scouters = 0.8
        self.height_threshold = 10

    def distance_tiles(self, tileA, tileB):
        return self.distance(tileA.x, tileA.y, tileB.x, tileB.y) 

    def distance(self, xA, yA, xB, yB):
        return math.sqrt((xA - xB)**2 + (yA - yB)**2)
    
    def update_interval_recycler(self):
        if self.height > self.height_threshold:
            if self.turn < 10:
                self.interval_recycler = 2
            elif self.turn < 20:
                self.interval_recycler = 10
            elif self.turn < 40:
                self.interval_recycler = 1000

            if self.turn < 15:
              self.ratio_scouters = 1
            elif self.turn < 30:
                self.ratio_scouters = 0.5
        else:
            if self.turn < 10:
                self.interval_recycler = 3
            elif self.turn < 20:
                self.interval_recycler = 10
            elif self.turn < 40:
                self.interval_recycler = 1000

            if self.turn < 10:
                self.ratio_scouters = 1
            elif self.turn < 20:
                self.ratio_scouters = 0.5

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

    def get_closest_tile_from_opponent_tile(self, opponent_tile):
        return self.get_extreme_tile(opponent_tile, self.inputs.my_tiles)

    def total_scrap_amount_of_adjacent_tiles(self, tile):
        if tile.x > 0 and tile.x < self.width-1 and tile.y > 0 and tile.y < self.height-1:     
            return tile.scrap_amount  + self.inputs.tiles[tile.y-1][tile.x].scrap_amount + self.inputs.tiles[tile.y+1][tile.x].scrap_amount + self.inputs.tiles[tile.y][tile.x-1].scrap_amount + self.inputs.tiles[tile.y][tile.x+1].scrap_amount
        return 0

    def is_tile_near_recycler(self,tile):
        for recycler in self.inputs.my_recyclers:
            if (recycler.x == tile.x and abs(recycler.y-tile.y)<=2) or (recycler.y == tile.y and abs(recycler.x-tile.x)<=2) or (abs(recycler.x-tile.x)==1 and abs(recycler.y-tile.y)==1):
                return True
        return False

    def get_best_recycler_tile(self):
        list_eligible_tiles = list(filter(lambda tile: tile.can_build() and not tile.has_units() and (not self.is_tile_near_recycler(tile)), self.inputs.my_tiles))
        if len(list_eligible_tiles) > 0:
            list_scrap_amounts = list(map(lambda tile : self.total_scrap_amount_of_adjacent_tiles(tile), list_eligible_tiles ))
            best_recycler_location_index = np.argmax(list_scrap_amounts)
            return list_eligible_tiles[best_recycler_location_index]
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

    def play(self):
        actions = []
        if self.turn > 2 and self.turn % self.interval_recycler == 0 :
            if self.inputs.my_matter >= 10:
                tile = self.get_best_recycler_tile()
                if tile != None:
                    actions.append('BUILD {} {}'.format(tile.x, tile.y))
                    self.inputs.my_matter -= 10
        if self.inputs.my_matter >= 10:
            opponent_center = self.get_opponent_center()
            if opponent_center != None:
                closest_tile_from_opponent_tile = self.get_closest_tile_from_opponent_tile(opponent_center)
                if closest_tile_from_opponent_tile != None and closest_tile_from_opponent_tile.can_spawn(): # TODO : Find another location here if we can't build
                    amount = self.inputs.my_matter // 10  
                    if amount > 0:
                        actions.append('SPAWN {} {} {}'.format(
                            amount, closest_tile_from_opponent_tile.x, closest_tile_from_opponent_tile.y))
       
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
