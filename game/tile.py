import pyglet
import resources

colors = {
    "black":resources.tile_black,
    "grey":resources.tile_grey,
    "blue":resources.tile_blue,
    "stair":resources.stair,
}

class Tile(pyglet.sprite.Sprite):
    def __init__(self,color, *args, **kwargs):
        super(Tile, self).__init__(img=colors[color],*args, **kwargs)
        self.initial_x = self.x
        self.initial_y = self.y
        self.visited = False
        self.inside = []

    def set_opacity(self, opacity):
        for sprite in self.inside:
            if opacity != 255:
                sprite.opacity = 0
            else:
                sprite.opacity = opacity
        self.opacity = opacity

    def attach(self, sprite):
        self.inside.append(sprite)

    def detach(self, sprite):
        self.inside.remove(sprite)
