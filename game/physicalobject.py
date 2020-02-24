import pyglet
import utils

class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        self.velocity_x = 0
        self.velocity_y = 0
        self.dead = False
        self.new_objects = []

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2
        max_x = 800 + self.image.width/2
        max_y = 600 + self.image.height/2
        if self.x < min_x:
            self.x = max_x 
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y: 
            self.y = max_y 
        elif self.y > max_y: 
            self.y = min_y

    def collides_with(self, obj):
        min_distance = self.image.width/2 + self.image.width/2
        col_distance = utils.distance(self.position, obj.position)
        return col_distance < min_distance

    def handle_collision_with(self, obj):
        if type(self) == type(obj):
            self.dead = False
        else:
            self.dead = True

        

