import pyglet
import maps
import skill
from pyglet.window import key

class Overlay(object):
    def __init__(self, world):
        self.world = world
        self.title = pyglet.text.Label(text="Menu",x=maps.TILE_SIZE*maps.TILES_X/2,y=maps.TILES_Y*maps.TILE_SIZE - 30, anchor_y="center")

    def draw(self):
        pyglet.gl.glColor4f(255,0,0,0.8)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
            ('v2i', (500, 0, 500, 550))                                                
        )
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
            ('v2i', (0, 550, 800, 550))                                                
        )
        self.title.draw()

    def update(self, dt):
        pass

    def on_key_release(self, symbol, modifiers):
        if symbol == key.BACKSPACE:
            self.world.overlay = None


class LevelUpOverlay(Overlay):
    def __init__(self, *args, **kwargs):
        super(LevelUpOverlay, self).__init__(*args, **kwargs)
        self.selected = 0
        self.items = []
        self.items_label = []
        self.title.text = "LEVEL UP - Choose a new ability wisely"
        self.usage = pyglet.text.Label(x=510, y=520,multiline=True, width=240)
        self.usage.text = "AROWS to navigate\nENTER to choose"
        self.item_description = pyglet.text.Label(x=510, y=430,multiline=True, width=240)
        self.init_items()
        
    def reinit(self):
        self.items = []
        self.items_label = []
        self.selected = 0
        self.init_items()
        
    def init_items(self):
        skills = [skill.Strengh(), skill.Armor(), skill.Dexterity()]
        player = self.world.player
        i = 0
        for item in skills:
            self.items.append(item)
            new_label = pyglet.text.Label(x=10, y=520-i*20, text=item.name)
            self.items_label.append(new_label)
            i += 1

    def draw(self):
        super(LevelUpOverlay, self).draw()
        pyglet.gl.glColor4f(255,0,0,0.8)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
            ('v2i', (500, 450, 800, 450))
        )
        self.usage.draw()
        self.item_description.draw()
        for label in self.items_label:
            label.draw()

    def update(self, dt):
        if not self.items:
            return
        for label in self.items_label:
            if label == self.items_label[self.selected]:
                self.items_label[self.selected].color = (255,255,0,255)
                self.item_description.text = self.items[self.selected].description
            else:
                label.color = (255,255,255,255)

    def on_key_release(self, symbol, modifiers):
        super(LevelUpOverlay, self).on_key_release(symbol,modifiers)
        if symbol == key.DOWN:
            if self.selected < len(self.items)-1:
                self.selected += 1
            else:
                self.selected = 0
        if symbol == key.UP:
            if self.selected > 0:
                self.selected -= 1
            else:
                self.selected = len(self.items)-1
        if symbol == key.ENTER:
            # TODO player got his skill
            self.world.overlay = None

class InventoryOverlay(Overlay):
    def __init__(self, *args, **kwargs):
        super(InventoryOverlay, self).__init__(*args, **kwargs)
        self.selected = 0
        self.items = []
        self.items_label = []
        self.title.text = "INVENTORY"
        self.usage = pyglet.text.Label(x=510, y=520,multiline=True, width=240)
        self.usage.text = "AROWS to navigate\nENTER to equip\nD to drop(not working)\nBACKSPACE to exit"
        self.item_description = pyglet.text.Label(x=510, y=430,multiline=True, width=240)
        self.init_items()

    def reinit(self):
        self.items = []
        self.items_label = []
        self.selected = 0
        self.init_items()

    def init_items(self):
        player = self.world.player
        i = 0
        for item in player.pack:
            self.items.append(item)
            new_label = pyglet.text.Label(x=10, y=520-i*20, text=item.name)
            self.items_label.append(new_label)
            i += 1

    def draw(self):
        super(InventoryOverlay, self).draw()
        pyglet.gl.glColor4f(255,0,0,0.8)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
            ('v2i', (500, 450, 800, 450))
        )
        self.usage.draw()
        self.item_description.draw()
        for label in self.items_label:
            label.draw()

    def update(self, dt):
        if not self.items:
            return
        for label in self.items_label:
            if label == self.items_label[self.selected]:
                self.items_label[self.selected].color = (255,255,0,255)
                self.item_description.text = self.items[self.selected].description
            else:
                label.color = (255,255,255,255)

    def on_key_release(self, symbol, modifiers):
        super(InventoryOverlay, self).on_key_release(symbol,modifiers)
        if symbol == key.DOWN:
            if self.selected < len(self.items)-1:
                self.selected += 1
            else:
                self.selected = 0
        if symbol == key.UP:
            if self.selected > 0:
                self.selected -= 1
            else:
                self.selected = len(self.items)-1
        if symbol == key.ENTER:
            if self.items and self.world.player.equip(self.items[self.selected]):
                self.world.overlay = None


class MenuOverlay(Overlay):
    def __init__(self, *args, **kwargs):
        super(MenuOverlay, self).__init__(*args, **kwargs)
        self.title.text = "Menu"

