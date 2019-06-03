import pygame as pg
import traceback

TILESIZE_W = 32
TILESIZE_H = 32

def add_bin(a, b):
    # adds two binary strings together
    return bin(int(a, 2) + int(b, 2))

def bool_list_to_mask(bools):
    mask_string = ''.join(['{:d}'.format(b) for b in bools])
    return int(mask_string, 2)


BLUE = (72, 215, 216) # sea blue for the background


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((512, 512))
        self.clock = pg.time.Clock()
        
        self.show_grid = False
        
        # load tileset
        self.tileset_image = pg.image.load('autotiles.png').convert()
        tiles_w = int(self.tileset_image.get_width() / TILESIZE_W)
        tiles_h = int(self.tileset_image.get_height() / TILESIZE_H)
        
        self.tileset = []
        # load tiles as subsurfaces from a tileset image
        for i in range(tiles_w * tiles_h):
            r = (i % tiles_w * TILESIZE_W, int(i / tiles_w) * TILESIZE_H,
                 TILESIZE_W, TILESIZE_H)
            self.tileset.append(self.tileset_image.subsurface(r))
        
        # array of data that constructs the map
        self.map_data = [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0],
                [0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0],
                [0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0],
                [0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0],
                [0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0],
                [0,1,1,1,1,1,0,0,1,1,0,1,1,0,0,0],
                [0,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0],
                [0,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0],
                [0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,1,1,1,0,0,0,0,1,0,0],
                [0,0,1,1,1,0,1,1,1,1,1,1,0,1,0,0],
                [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                ]

        # bitmask-to-base10 values and the corresponding tile index
        self.tile_dict = {
                        2 : 1,
                        8 : 2, 
                        10 : 3, 
                        11 : 4, 
                        16 : 5, 
                        18 : 6, 
                        22 : 7, 
                        24 : 8,
                        26 : 9, 
                        27 : 10, 
                        30 : 11, 
                        31 : 12, 
                        64 : 13,
                        66 : 14, 
                        72 : 15, 
                        74 : 16, 
                        75 : 17, 
                        80 : 18, 
                        82 : 19, 
                        86 : 20, 
                        88 : 21, 
                        90 : 22, 
                        91 : 23, 
                        94 : 24, 
                        95 : 25, 
                        104 : 26, 
                        106 : 27, 
                        107 : 28, 
                        120 : 29, 
                        122 : 30, 
                        123 : 31, 
                        126 : 32, 
                        127 : 33, 
                        208 : 34, 
                        210 : 35, 
                        214 : 36, 
                        216 : 37, 
                        218 : 38, 
                        219 : 39, 
                        222 : 40, 
                        223 : 41, 
                        248 : 42,
                        250 : 43, 
                        251 : 44, 
                        254 : 45, 
                        255 : 46, 
                        0 : 47
                          }

        
    def construct_map(self):
        # create an empty surface for the map
        self.map_image = pg.Surface((len(self.map_data) * TILESIZE_W,
                                     len(self.map_data[0] * TILESIZE_H)))
        self.map_image.fill(BLUE)
        
        # loop through the map data array and blit the corresponding tile
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                # x and y are flipped because I loop through the vertical
                # component (columns) first
                if self.map_data[y][x]:
                    # calculate the bitmask if the tile is 1 (land)
                    bitmask = [False]*8
                    # loop over all neighbor tiles
                    if self.map_data[y - 1][x - 1]:
                        # check adjacent tiles to the west and south
                        # this is done to reduce the possible index values to 48 in total
                        if self.map_data[y - 1][x] and self.map_data[y][x - 1]:
                            bitmask[7] = True
                    if self.map_data[y - 1][x]:
                        bitmask[6] = True
                    if self.map_data[y - 1][x + 1]:
                        if self.map_data[y - 1][x] and self.map_data[y][x + 1]:
                            bitmask[5] = True
                    if self.map_data[y][x - 1]:
                            bitmask[4] = True
                    if self.map_data[y][x + 1]:
                        bitmask[3] = True
                    if self.map_data[y + 1][x - 1]:
                        if self.map_data[y + 1][x] and self.map_data[y][x - 1]:
                            bitmask[2] = True
                    if self.map_data[y + 1][x]:
                        bitmask[1] = True
                    if self.map_data[y + 1][x + 1]:
                        if self.map_data[y + 1][x] and self.map_data[y][x + 1]:
                            bitmask[0] = True
                        
                    key = bool_list_to_mask(bitmask)
                    try:
                        self.map_image.blit(self.tileset[self.tile_dict[key]],
                                       (x * TILESIZE_W, y * TILESIZE_H))
                    except KeyError:
                        # fail safe in case the calculated bitmask is wrong
                        # this is only for bugfixing
                        print('tile not found for {:08b}'.format(key))
                        s = pg.Surface((32, 32))
                        s.fill(pg.Color('red'))
                        self.map_image.blit(s, (x * TILESIZE_W, y * TILESIZE_H))
                        
    
    def update(self):
        mpos = pg.mouse.get_pos()
        
        tile_x = int(mpos[0] / TILESIZE_W)
        tile_y = int(mpos[1] / TILESIZE_H)
        if tile_y == len(self.map_data) - 1 or tile_x == len(self.map_data[0]) - 1:
            return
        
        if self.mouse_pressed[0]:
            # left mouse pressed
            self.map_data[tile_y][tile_x] = 1
            self.construct_map()
        if self.mouse_pressed[2]:
            # right mouse pressed
            self.map_data[tile_y][tile_x] = 0
            self.construct_map()
            
    
    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.screen.blit(self.map_image, (0, 0))
        
        tiles_w = self.screen.get_width() // TILESIZE_W
        tiles_h = self.screen.get_height() // TILESIZE_H
        
        if self.show_grid:
            color = pg.Color('white')
            for i in range(tiles_w):
                start = (i * TILESIZE_W, 0)
                end = (i * TILESIZE_W, self.screen.get_height())
                pg.draw.line(self.screen, color, start, end)
            for i in range(tiles_h):
                start = (0, i * TILESIZE_H)
                end = (self.screen.get_width(), i * TILESIZE_H)
                pg.draw.line(self.screen, color, start, end)
        
        pg.display.update()
        
        
    def run(self):
        self.construct_map()
        
        self.running = True
        while self.running:
            # reset mouse buttons
            self.mouse_pressed = [0, 0, 0, 0, 0]
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pressed[event.button - 1] = 1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:
                        self.show_grid = not self.show_grid
                    
            self.clock.tick(30)
            
            self.update()
            self.draw()
        
        pg.quit()
        
        

if __name__ == '__main__':
    try:
        g = Game()
        g.run()
    except:
        traceback.print_exc()
        pg.quit()