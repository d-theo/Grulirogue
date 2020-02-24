import pyglet
import physicalobject
import resources
import maps
import math

class Bullet(physicalobject.PhysicalObject):
    def __init__(self, type_bullet, *args, **kwargs):
        image = resources.bullet_image
        if type_bullet == 'Bow':
            image = resources.arrow_shot_image
        if type_bullet == 'Crossbow':
            image = resources.bolt_shot_image
        super(Bullet, self).__init__(img=image, *args, **kwargs)
        self.ttl = None
        self.dead = False
        self.speed = 100
        self.velocity_y = 0
        self.velocity_x = 0

    def update(self, dt):
        super(Bullet, self).update(dt)
        if self.should_die():
            self.dead = True

    def should_die(self):
        #out of bound
        if self.x < 0 or self.y < 0 or self.x > 800 or self.y > 600:
            return True
        if not self.ttl: 
            return

        #in the xycoord screen
        limitx = self.ttl[0] * maps.TILE_SIZE + maps.TILE_SIZE/2
        limity = self.ttl[1] * maps.TILE_SIZE + maps.TILE_SIZE/2
        
        dx = math.fabs(self.x - limitx)
        dy = math.fabs(self.y - limity)

        if dx < 7 or dy < 7:
            return True
        
        return False
