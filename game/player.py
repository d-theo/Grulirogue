import pyglet
import physicalobject
import resources
import item
import random

XP_TABLE    = [0 for x in range(0,10)]
XP_TABLE[0] = 0
XP_TABLE[1] = 100
XP_TABLE[2] = 300
XP_TABLE[3] = 900
XP_TABLE[4] = 1200
XP_TABLE[5] = 1800
XP_TABLE[6] = 2500
XP_TABLE[7] = 5000


class Player(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        self.pack = []
        self.lweapon = item.Item.factory("Slingshot")
        self.rweapon = None
        self.selected = self.lweapon

        self.lif = 100
        self.max_lif = 100
        self.dex = 1
        self.atk = 0
        self.amr = 0
        self.xp = 0
        self.level = 0

        self.moved = False

        self.ring = None

    def get_xp(self):
        return 100*self.xp / XP_TABLE[self.level+1]

    def add_xp(self, xp):
        self.xp += xp
        if self.xp >= XP_TABLE[self.level+1]:
            rest = XP_TABLE[self.level+1] - self.xp
            self.level += 1
            self.xp = rest
            return True
        return False

    def get_dex(self):
        modifier = self.dex
        if self.moved:
            modifier += 3
        if self.ring and self.ring.modifier_type == "dex":
            modifier += self.ring.modifier
        return modifier

    def get_atk(self):
        modifier = self.atk
        if self.ring and self.ring.modifier_type == "atk":
            modifier += self.ring.modifier
        return modifier

    def get_amr(self):
        modifier = self.amr
        if self.ring and self.ring.modifier_type == "amr":
            modifier += self.ring.modifier
        return modifier

    def get_max_lif(self):
        modifier = self.max_life
        if self.ring and self.ring.modifier_type == "lif":
            modifier += self.ring.modifier
        return modifier

    def add_item(self, new_item):
        if len(self.pack) > 10:
            return False
        else:
            self.pack.append(new_item)
            return True

    def get_dmg(self):
        modifier = self.get_atk()
        return random.randint(self.selected.dmg[0],self.selected.dmg[1]) + modifier

    def swap_weapon(self):
        if self.selected == self.lweapon:
            self.selected = self.rweapon
        else:
            self.selected = self.lweapon

    def reload_weapon(self):
        reloaded = False
        for i in range(self.selected.total):
            for item in self.pack:
                if isinstance(item, self.selected.bullet):
                    reloaded = True
                    item.count -= 1
                    self.selected.count += 1
                    item.update_name()
                    if item.count == 0:
                        self.pack.remove(item)
                    break
        return reloaded
    
    def equip(self, item):
        old_item = None
        if item.typeitem == "nothing":
            return False
        elif item.typeitem == "weapon":
            if self.selected == self.lweapon:
                old_item = self.lweapon
                self.lweapon = item
                self.selected = self.lweapon
            else:
                old_item = self.rweapon
                self.rweapon = item
                self.selected = self.rweapon
            self.pack.remove(item)
            self.pack.append(old_item)
        elif item.typeitem == "consumable":
            self.consume(item)
        elif item.typeitem == "wear":
            print ("wear")
            self.wear(item)

        return True

    def consume(self, item):
        if type(item).__name__ == "Health":
            self.lif += 20
            if self.lif > self.max_lif:
                self.lif = self.max_lif
            self.pack.remove(item)

    def wear(self, item):
        if item.subtype == "ring":
            if self.ring:
                self.pack.append(self.ring)
            self.pack.remove(item)
            self.ring = item

    def weapon_log(self):
        log = 'Weapon 1 : ' + self.selected.name +'('+str(self.selected.dmg[0])+'-'+str(self.selected.dmg[1])+')'
        if self.selected.total != -1:
            log += " "+str(self.selected.count)+"/"+str(self.selected.total)
        if self.selected.count == 0:
            return (log, (255,0,0,255))
        else:
            return (log, (255,255,0,255))

