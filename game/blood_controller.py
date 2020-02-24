class BloodController(object):
    def __init__(self):
        self.blood = []

    def clear(self):
        self.blood = []

    def add_bloods(self, bloods):
        self.blood.extend(bloods)

    def add_blood(self, blood):
        self.blood.append(blood)

    def update(self, dt, themap):
        for b in self.blood:
            b.update(dt,themap)

    def draw(self):
        for b in self.blood:
            b.draw()
