import numpy as np

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

        # print(diffusion_matrix, file=sys.stderr, flush=True)
        return diffusion_matrix