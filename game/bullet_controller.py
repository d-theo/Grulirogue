class BulletsController(object):
    def __init__(self):
        self.bullets = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def clear_bullets(self):
        self.bullets = []

    def update(self, dt):
        for b in self.bullets:
            if b.dead:
                self.bullets.remove(b)
            else:
                b.update(dt)

    def draw(self):
        for b in self.bullets:
            b.draw()

