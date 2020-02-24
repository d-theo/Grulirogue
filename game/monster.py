import pyglet
import resources
import maps
import utils
import random
import math
import bullet
import loots
import item

map_type_bullet = {
    'Bow':'arrow',
    'Crossbow':'bolt',
}

class Monster(pyglet.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *args, **kwargs):
        super(Monster, self).__init__(*args, **kwargs)
        self.new_objects    = []
        self.loot           = []

        self.dead = False
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.difficulty = 1
        self.weapon = item.Item.factory("Bow")
        self.weapon_dmg = 3
        self.lif = 10
        self.dex = 0
        self.atk = 0
        self.amr = 0
        self.vision = 9
        self.shoot_vision = 7
        self.xp = 20

    def update(self, dt, world):
        self.x = self.pos_x * maps.TILE_SIZE - world.scroll_x * maps.TILE_SIZE
        self.y = self.pos_y * maps.TILE_SIZE - world.scroll_y * maps.TILE_SIZE

    def play(self, world, player):
        #if i see him i attack
        self.attack(world, player)
        world.infos = maps.LOG['under_attack']

    def move_to_target(self, world):
        target = (world.curr[0], world.curr[1])
        pos_x = -1 if self.pos_x - target[0] > 0 else 1
        pos_y = -1 if self.pos_y - target[1] > 0 else 1
        if utils.is_valid_move((self.pos_x+pos_x, self.pos_y+ pos_y), world, maps.SIZE):
            world.cases[self.pos_x][self.pos_y].detach(self)
            self.pos_x += pos_x
            self.pos_y += pos_y
            world.cases[self.pos_x][self.pos_y].attach(self)

    def move_random(self, world):
        if random.randint(0,100)>70:
            pos_x = random.randint(-1,1) 
            pos_y = random.randint(-1,1)
            if utils.is_valid_move((self.pos_x+pos_x,self.pos_y+pos_y), world, maps.SIZE):
                world.cases[self.pos_x][self.pos_y].detach(self)
                world.cases[pos_x+self.pos_x][pos_y+self.pos_y].attach(self)
                self.pos_x += pos_x
                self.pos_y += pos_y

    def defend(self,world,player):
        p_pos = (world.curr[0]-world.scroll_x, world.curr[1]-world.scroll_y)
        m_pos = (self.pos_x-world.scroll_x, self.pos_y-world.scroll_y)

        avoid = (self.dex - player.get_dex()) * 10 + 15
        avoid_roll = random.randint(0,100)
        if avoid > avoid_roll:
            self.fire(p_pos, m_pos, player.selected, True)
            world.infos = maps.LOG['def_miss']
            return

        dmg = player.get_dmg()
        output = dmg + player.get_atk() - self.amr
        self.lif -= output
        self.fire(p_pos, m_pos, player.selected)

        if self.lif <= 0:
            world.infos = maps.LOG['monster_die']
            self.loot = loots.get_loot(self.difficulty, self.pos_x, self.pos_y) + ['blood']
            self.dead = True
            if player.add_xp(self.xp):
                world.next_player_level()

    def attack(self, world, player):
        avoid = (player.get_dex() - self.dex) * 10 + 15
        avoid_roll = random.randint(0,100)
        if avoid > avoid_roll:
            self.fire((self.pos_x-world.scroll_x, self.pos_y-world.scroll_y), (world.curr[0]-world.scroll_x, world.curr[1]-world.scroll_y), self.weapon, True)
            world.infos = maps.LOG['atk_miss']
            return

        output = self.weapon_dmg + self.atk - player.get_amr()
        player.lif -= output

        self.fire((self.pos_x-world.scroll_x, self.pos_y-world.scroll_y), (world.curr[0]-world.scroll_x, world.curr[1]-world.scroll_y ), self.weapon)
        world.infos = maps.LOG['player_hit']


    def get_info(self):
        return 'a basic monster'

    def fire(self, c_init, c_end, type_bullet, miss=False):
        angle_radian = math.atan2(c_end[1] - c_init[1] , c_end[0] - c_init[0])
        fx = math.cos(angle_radian) * 800
        fy = math.sin(angle_radian) * 800
        new_bullet = bullet.Bullet(type(type_bullet).__name__, x=c_init[0]*maps.TILE_SIZE+12, y=c_init[1]*maps.TILE_SIZE+12)
        new_bullet.velocity_x = fx
        new_bullet.velocity_y = fy
        new_bullet.rotation = -(math.degrees(angle_radian) - 90)
        if not miss:
            new_bullet.ttl = c_end
        self.new_objects.append(new_bullet)

################################
########Type Monsters
################################

class Gobelin(Monster):
    def __init__(self,*args, **kwargs):
        super(Gobelin, self).__init__(img=resources.gobelin_image, *args, **kwargs)
        self.weapon = item.Item.factory("Bow")
        self.weapon_dmg = 2
        self.lif = 5
        self.dex = 0
        self.atk = 0
        self.amr = 0
        self.vision = 9
        self.shoot_vision = 7
        self.xp = 15
        self.difficulty = 1

class Skeleton(Monster):
    def __init__(self, *args, **kwargs):
        super(Skeleton, self).__init__(img=resources.archer_image, *args, **kwargs)
        self.weapon = item.Item.factory("Bow")
        self.weapon_dmg = 3
        self.lif = 10
        self.dex = 0
        self.atk = 0
        self.amr = 0
        self.vision = 9
        self.shoot_vision = 7
        self.xp = 20
        self.difficulty = 2
