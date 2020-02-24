import item
import random

class Loot:
    def __init__(self):
        self.loot_table = ["" for x in range(100)]

    def add_loot(self, loot, probability):
        cpt = 0
        for i in range(len(self.loot_table)):
            if self.loot_table[i] == '':
                self.loot_table[i] = loot
                cpt += 1
            if cpt == probability:
                break
    
    def rand_loot(self):
        randloot = random.randint(0, 99)
        return self.loot_table[randloot]

#1 gobelin
archer = Loot()
archer.add_loot("Arrow",25)
archer.add_loot("Bow",5)

#2 skel
skel = Loot()
skel.add_loot("Arrow",10)
skel.add_loot("Bow",10)

#11 weapon niveau 1
item1 = Loot()
item1.add_loot("Bow",50)
item1.add_loot("Arrow",50)

#21 weapon niveau 1
item2 = Loot()
item2.add_loot("Bow",25)
item2.add_loot("Arrow",25)
item2.add_loot("Bolt",25)
item2.add_loot("Crossbow",25)

#12 item niveau 1
item12 = Loot()
item12.add_loot("Health",60)
item12.add_loot("MinRingDex",10)
item12.add_loot("MinRingLif",10)
item12.add_loot("MinRingAmr",10)
item12.add_loot("MinRingAtk",10)

def get_loot(difficulty, pos_x, pos_y):
# level1
    if difficulty == 1:
        drop = archer
    if difficulty == 11:
        drop = item1
    if difficulty == 12:
        drop = item12
# level2
    if difficulty == 2:
        drop = skel
    if difficulty == 21:
        drop = item2
    if difficulty == 22:
        drop = item12
#level3
    if difficulty == 3:
        drop = skel
    if difficulty == 31:
        drop = item2
    if difficulty == 32:
        drop = item12

    loot = drop.rand_loot()
    if loot != "":
        return [item.Item.factory(loot, pos_x, pos_y)]

    return []
