import tile
import pyglet
import resources
import overlay
import mapitem
import utils
import mapcreator
import cProfile
#cProfile.runctx('self.set_sight()',globals(),locals())
from pyglet.window import key

SIZE = 50
TILE_SIZE = 25
TILES_X = 32
TILES_Y = 24
COOLDOWN = 5
COOLDOWN_OVERLAY = 60

LOG = {
    'wall':"A wall is blocking you",
    'death':"You die",
    'nothing':"",
    'under_attack':"You are under attack",
    'def_miss':"The monster dodged your attack",
    'atk_miss':"You dodged the attack",
    'player_hit':'aouch!',
    'monster_die':'You killed the monster !',
    'item_desc':'There is a ',
    'item_take':'You took the ',
    'stair':'Stairs, S to enter',
}

MAPING = {
    '0':'empty',
    'X':'wall',
}

class Map:
    def __init__(self, player, current_level, difficulty_level, batch):
        self.current_level = current_level
        self.difficulty_level = difficulty_level
        self.go_next_level = False
        self.player = player
        self.init_overlays()
        self.overlay = None
        self.batch = batch
        self.player_turn = True
        self.curr     = [TILES_X/2, TILES_Y/2]
        self.scroll_x = 0
        self.scroll_y = 0
        self.init_scrolling()
        self.cooldown = 0
        self.tiles = [[0 for x in range(SIZE)] for x in range(SIZE)] 
        self.cases = [[0 for x in range(SIZE)] for x in range(SIZE)]
        self.init_map()
        self.parse_map()
        self.init_view()
        self.all_items   = mapitem.MapItem(self)

        self.key_handler = key.KeyStateHandler()

        self.center = (TILES_X/2*TILE_SIZE, TILES_Y/2*TILE_SIZE)
        self.infos  = "Nouvelle partie"
        self.update_fog()
        self.set_sight(True)

    def drawItems(self):
        self.all_items.draw()

    def init_scrolling(self):
        for x in range(SIZE):
            for y in range(SIZE):
                if self.current_level[x][y] == 'i':
                    self.scroll_x = x-self.curr[0]
                    self.scroll_y = y-self.curr[1]
                    self.curr = [x,y]


    def init_overlays(self):
        self.overlays = {
            "inventory":overlay.InventoryOverlay(self),
            "menu":overlay.MenuOverlay(self),
            "level_up":overlay.LevelUpOverlay(self),
        }

    def init_map(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.current_level[i][j] != 'X':
                    self.tiles[i][j] = 0
                else:
                    self.tiles[i][j] = 'X'

    def init_view(self):
        self.viewport = []
        port = []
        for i in range(SIZE):
            for j in range(SIZE):
                if i >= self.scroll_x-8 and i < self.scroll_x+TILES_X+8 and j >= self.scroll_y-6 and j < self.scroll_y + TILES_Y+6:
                    self.cases[i][j].x = self.cases[i][j].initial_x - self.scroll_x * TILE_SIZE
                    self.cases[i][j].y = self.cases[i][j].initial_y - self.scroll_y * TILE_SIZE
                    port.append(self.cases[i][j])
        self.viewport = port
                

    def parse_map(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j] == 'X':
                    self.cases[i][j] = tile.Tile("grey", x=i*TILE_SIZE , y=j*TILE_SIZE, batch=self.batch)
                elif self.current_level[i][j] == "f":
                    self.cases[i][j] = tile.Tile("stair",x=i*TILE_SIZE ,y=j*TILE_SIZE, batch=self.batch)
                elif self.tiles[i][j] == 0:
                    self.cases[i][j] = tile.Tile("blue",x=i*TILE_SIZE ,y=j*TILE_SIZE, batch=self.batch)

    def set_player_turn(self, turn):
        if not turn:
            self.cooldown = COOLDOWN
        self.player_turn = turn

    def set_player_moved(self, boolean):
        self.player.moved = boolean

    def update_cd(self):
        if self.cooldown > 0:
            self.cooldown -=1

    def is_on_cd(self):
        return self.cooldown > 0

    def update(self, dt):
        self.update_cd()
        self.all_items.update(dt)
        
        #check moves
        moved = False
        if self.key_handler[key.UP]:
            if self.is_move_allowed('up'):
                self.scroll_y += 1
                self.curr[1]  += 1
                moved = True
        if self.key_handler[key.DOWN]:
            if self.is_move_allowed('down'):
                self.scroll_y -= 1
                self.curr[1]  -= 1
                moved = True
        if self.key_handler[key.LEFT]:
            if self.is_move_allowed('left'):
                self.scroll_x -= 1
                self.curr[0]  -= 1
                moved = True
        if self.key_handler[key.RIGHT]:
            if self.is_move_allowed('right'):
                self.scroll_x += 1
                self.curr[0]  += 1
                moved = True
        if moved:
            self.update_fog()
            self.infos = LOG['nothing']
            self.init_view()
            self.set_player_moved(True)
            self.set_player_turn(False)

        if self.current_level[self.curr[0]][self.curr[1]] == 'f':
            self.infos = LOG["stair"]
        if self.key_handler[key.S]:
            if self.current_level[self.curr[0]][self.curr[1]] == 'f':
                self.go_next_level = True

        #check for items on the ground
        ground_item = self.check_items()
        if ground_item:
            self.infos = LOG['item_desc'] + ground_item.name
            if self.key_handler[key.T]:
                if self.player.add_item(ground_item):
                    self.all_items.remove_item(ground_item)
                    try:
                        self.cases[self.curr[0]][self.curr[0]].detach(ground_item)
                    except ValueError:
                        pass # or scream: thing not in some_list!
                    self.infos = LOG['item_take'] + ground_item.name


    def check_items(self):
        ground_item = self.all_items.item_at(self.curr[0], self.curr[1])
        if ground_item:
            return ground_item
        return None


    def is_move_allowed(self, direction):
        if self.is_on_cd():
            return False

        x = self.curr[0]
        y = self.curr[1]
        if direction == 'up':
            if self.tiles[x][y+1] != 'X':
                return True
        if direction == 'down':
            if self.tiles[x][y-1] != 'X':
                return True
        if direction == 'left':
            if self.tiles[x-1][y] != 'X':
                return True
        if direction == 'right':
            if self.tiles[x+1][y] != 'X':
                return True
        self.infos = LOG['wall']
        return False

    def on_key_release(self, symbol, modifiers):
        if symbol == key.I:
            self.overlays['inventory'].reinit()
            self.overlay = self.overlays['inventory']
        if symbol == key.M:
            self.overlay = self.overlays['menu']
    
    def update_fog(self):
        disc = utils.disc_from_circle(self.curr[0], self.curr[1], 10)
        disc = utils.filter_valid(disc, SIZE)
        inside = self.in_range(disc)
        self.set_sight()
        self.set_visible(inside)

    def set_sight(self, repaint=False):
        if repaint:
            xmax = ymax = SIZE
            xmin = ymin = 0
        else:
            xmin = self.curr[0]-16 if self.curr[0]-16 >=0 else 0
            xmax = self.curr[0]+16 if self.curr[0]+16 < SIZE else SIZE-1
            ymin = self.curr[1]-12 if self.curr[1]-12 >=0 else 0
            ymax = self.curr[1]+12 if self.curr[1]+12 < SIZE else SIZE-1
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                self.cases[i][j].set_opacity(0)
                if self.cases[i][j].visited:
                    self.cases[i][j].set_opacity(200)

    def set_visible(self, inside):
        for tile in inside:
            x=tile[0]
            y=tile[1]
            self.cases[x][y].set_opacity(255)
            self.cases[x][y].visited = True

    def in_range(self, circle):
        to_add = []
        for tile in circle:
            if utils.can_see_point(self.curr[0], self.curr[1], tile[0], tile[1], self.tiles):
                to_add.append(tile)
        return to_add

    def make_unique(self,original_list):
        unique_list = []
        [unique_list.append(obj) for obj in original_list if obj not in unique_list]
        return unique_list
    
    def next_player_level(self):
        self.overlays['level_up'].reinit()
        self.overlay = self.overlays['level_up']

