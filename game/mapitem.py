import pyglet
import math
import item
import maps
import loots

class MapItem(object):
    def __init__(self, world):
        self.world = world
        self.items = []
        self.init_items()

    def init_items(self):
        level = self.world.difficulty_level
        weapon = str(level) + '1'
        item = str(level) + '2'
        for x in range(maps.SIZE):
            for y in range(maps.SIZE):
                if self.world.current_level[x][y] == 'w':
                    new_item = loots.get_loot(int(weapon), x, y)[0]
                    self.items.append(new_item)
                    self.world.cases[x][y].attach(new_item)
                if self.world.current_level[x][y] == 'l':
                    new_item = loots.get_loot(int(item), x, y)[0]
                    self.items.append(new_item)
                    self.world.cases[x][y].attach(new_item)

    def update(self,dt):
        for item in self.items:
            item.update(dt, self.world)

    def draw(self):
        for item in self.items:
            item.draw()

    def item_at(self, x, y):
        for item in self.items:
            if item.pos_x == x and item.pos_y == y:
                return item
        return None
    
    def get_info(self, x, y):
        item = self.item_at(x,y)
        if item:
            return item.name
        else:
            return ''

    def remove_item(self, rm_item):
        self.items.remove(rm_item)

    def add_items(self, iterable):
        for i in iterable:
            self.add_item(i)

    def add_item(self, new_item):
        ok = True
        for item in self.items:
            if new_item.pos_x == item.pos_x and new_item.pos_y == item.pos_y:
                ok = False
        while not ok:
            rmin = -1
            rmax = 2
            for x in range(rmin, rmax):
                for y in range(rmin, rmax):
                    if self.is_available(new_item.pos_x+x,new_item.pos_y+y) and not ok:
                        new_item.pos_x += x
                        new_item.pos_y += y
                        ok = True
            if not ok:
                rmin -= 1
                rmax += 1
        self.items.append(new_item)

    def is_available(self,x,y):
        for item in self.items:
            if x == item.pos_x and y == item.pos_y:
                return False
        if self.world.tiles[x][y] == 'X':
            return False

        return True



