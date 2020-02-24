import pyglet
import maps
import resources

class Item(pyglet.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0, batch=None, *args, **kwargs):
        super(Item, self).__init__(batch=batch, *args, **kwargs)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.typeitem = "nothing"
        self.shake = 0

    def update(self, dt, world):
        self.x = self.pos_x * maps.TILE_SIZE - world.scroll_x * maps.TILE_SIZE
        self.y = self.pos_y * maps.TILE_SIZE - world.scroll_y * maps.TILE_SIZE

    @staticmethod
    def factory(type,x=0,y=0,batch=None):
        if type == "Slingshot":
            return Slingshot(x,y)
        if type == "Crossbow":
            return Crossbow(x,y)
        if type == "Blood":
            return Blood(x,y, batch)
        if type == "Bolt":
            return Bolt(x,y)
        if type == "Bow":
            return Bow(x,y)
        if type == "Arrow":
            return Arrow(x,y)
        if type == "Health":
            return Health(x,y)
        if type == "MinRingDex":
            return MinRingDex(x,y)
        if type == "MinRingLif":
            return MinRingLif(x,y)
        if type == "MinRingAtk":
            return MinRingAtk(x,y)
        if type == "MinRingAmr":
            return MinRingAmr(x,y)
        else:
            print ('TYPE INCONNU')

class Slingshot(Item):
    def __init__(self, *args, **kwargs):
        super(Slingshot, self).__init__(img=resources.crossbow_image, *args, **kwargs)
        self.name = "Slingshot"
        self.description = "A quality slingshot ! You may have difficulties to kill something with it but you definitly have plenty of rocks on the ground"
        self.dmg = (2,5)
        self.typeitem = "weapon"
        self.total = -1
        self.count = -1

class Crossbow(Item):
    def __init__(self, *args, **kwargs):
        super(Crossbow, self).__init__(img=resources.crossbow_image, *args, **kwargs)
        self.name = "Crossbow"
        self.description = "A nice crossbow, it can pierce even strong armors to do a lot of dammages but try to don't get hurt while you reload !"
        self.dmg = (15,20)
        self.typeitem = "weapon"
        self.total = 1
        self.count = 1
        self.shake = 5
        self.bullet = Bolt

class Bolt(Item):
    def __init__(self, *args, **kwargs):
        super(Bolt, self).__init__(img=resources.bolt_image, *args, **kwargs)
        self.description = "Perfectly sized for a crossbow ! Wait, does this little thing really hurts ?"
        self.count = 5
        self.name = str(self.count) + " bolts"

    def update_name(self):
        self.name = str(self.count) + " bolts"

class Bow(Item):
    def __init__(self, *args, **kwargs):
        super(Bow, self).__init__(img=resources.bow_image, *args, **kwargs)
        self.name = "Bow"
        self.description = "Standard bow. Reliable if you have enought strength to pull the string"
        self.dmg = (4,9)
        self.typeitem = "weapon"
        self.total = 5
        self.count = 5
        self.shake = 0
        self.bullet = Arrow

class Arrow(Item):
    def __init__(self, *args, **kwargs):
        super(Arrow, self).__init__(img=resources.arrow_image, *args, **kwargs)
        self.description = "A quiver used to carry some arrows..."
        self.count = 5
        self.name = str(self.count) + " arrows in the quiver"

    def update_name(self):
        self.name = str(self.count) + " arrows in the quiver"

class Arquebus(Item):
    def __init__(self, *args, **kwargs):
        super(Arquebus, self).__init__(img=resources.arquebuse_image, *args, **kwargs)
        self.name = "Arquebus"
        self.description = "Wow, it's a nice quality weapon made of wood and iron. This thing seems to be as deadly as the shot is loud"
        self.dmg = (30,50)
        self.typeitem = "weapon"
        self.total = 1
        self.count = 1
        self.shake = 10
        self.bullet = Bullet

class Bullet(Item):
    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(img=resources.bullet_image, *args, **kwargs)
        self.description = "Iron bullet that fits in a arquebus"
        self.count = 10
        self.name = str(self.count) + " bullets"

    def update_name(self):
        self.name = str(self.count) + " bullets"


#items
class Health(Item):
    def __init__(self, *args, **kwargs):
        super(Health, self).__init__(img=resources.health_image, *args, **kwargs)
        self.name = "Health kit"
        self.description = "Everything is here to fix your wounds"
        self.typeitem = "consumable"
        self.total = 1
        self.count = 1

class MinRingLif(Item):
    def __init__(self, *args, **kwargs):
        super(MinRingLif, self).__init__(img=resources.min_lif_ring_img, *args, **kwargs)
        self.name = "blue ring"
        self.description = "This ring looks a bit old"
        self.typeitem = "wear"
        self.subtype = "ring"
        self.modifier_type = "lif"
        self.modifier = 10

class MinRingDex(Item):
    def __init__(self, *args, **kwargs):
        super(MinRingDex, self).__init__(img=resources.min_dex_ring_img, *args, **kwargs)
        self.name = "green ring"
        self.description = "This ring is oddly light"
        self.typeitem = "wear"
        self.subtype = "ring"
        self.modifier_type = "dex"
        self.modifier = 1

class MinRingAtk(Item):
    def __init__(self, *args, **kwargs):
        super(MinRingAtk, self).__init__(img=resources.min_atk_ring_img, *args, **kwargs)
        self.name = "red ring"
        self.description = "This ring shine of a red light that makes you more confident"
        self.typeitem = "wear"
        self.subtype = "ring"
        self.modifier_type = "atk"
        self.modifier = 1

class MinRingAmr(Item):
    def __init__(self, *args, **kwargs):
        super(MinRingAmr, self).__init__(img=resources.min_amr_ring_img, *args, **kwargs)
        self.name = "grey ring"
        self.description = "It looks hard to break"
        self.typeitem = "wear"
        self.subtype = "ring"
        self.modifier_type = "amr"
        self.modifier = 1

#not droppable
class Blood(Item):
    def __init__(self, *args, **kwargs):
        super(Blood, self).__init__(img=resources.blood_image, *args, **kwargs)
