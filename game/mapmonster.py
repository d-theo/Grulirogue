import monster
import maps
import math
import utils
import item

class MapMonster:
    def __init__(self, world):
        self.world = world
        self.monsters = []
        self.init_mobs()

    def init_mobs(self):
        for x in range(maps.SIZE):
            for y in range(maps.SIZE):
                if self.world.current_level[x][y] == 'e':
                    new_monster = monster.Gobelin(x,y)
                    self.world.cases[x][y].attach(new_monster)
                    self.monsters.append(new_monster)
                elif self.world.current_level[x][y] == 'e1':
                    new_monster = monster.Skeleton(x,y)
                    self.world.cases[x][y].attach(new_monster)
                    self.monsters.append(new_monster)

    def draw(self):
        for m in self.monsters:
            m.draw()

    def getbullets(self):
        bullets = []
        for m in self.monsters:
            for obj in m.new_objects:
                bullets.append(obj)
        return bullets


    def getloot(self):
        loots = []
        for m in self.monsters:
            for loot in m.loot:
                if loot != 'blood':
                    loots.append(loot)
        return loots
    
    def getblood(self, map_batch):
        bloods = []
        for m in self.monsters:
            for loot in m.loot:
                if loot == 'blood':
                    blood = item.Item.factory("Blood",m.pos_x, m.pos_y, batch=map_batch)
                    blood.opacity = 200
                    bloods.append(blood)
        return bloods


    def update(self, dt):
        for m in self.monsters:
            m.new_objects   = []
            m.loot          = []
            if m.dead:
                self.world.cases[m.pos_x][m.pos_y].detach(m)
        self.monsters = [m for m in self.monsters if not m.dead and not m.loot]
        for monster in self.monsters:
            monster.update(dt, self.world)

    def actions(self, player):
        #selectionner les mobs en range
        #selectionner les mobs qui nous voit
        #faire une ou plusieurs action
        in_range = [m for m in self.monsters if self.has_range(m)]
        in_sight = [m for m in in_range if self.has_sight(m)]
        for monster in self.monsters:
            if monster in in_sight:
                if self.can_shoot(monster):
                    monster.play(self.world, player)
                else:
                    monster.move_to_target(self.world)
            else:
                monster.move_random(self.world)

    def can_shoot(self, monster):
        player_pos = (self.world.curr[0], self.world.curr[1])
        if math.fabs(player_pos[0]-monster.pos_x) <= monster.shoot_vision and math.fabs(player_pos[1]-monster.pos_y) <= monster.shoot_vision:
            return True
        return False

    def has_range(self, monster):
        player_pos = (self.world.curr[0], self.world.curr[1])
        if math.fabs(player_pos[0]-monster.pos_x) <= monster.vision and math.fabs(player_pos[1]-monster.pos_y) <= monster.vision:
            return True
        return False

    def has_sight(self, monster):
        return utils.can_see_point(monster.pos_x, monster.pos_y, self.world.curr[0], self.world.curr[1], self.world.tiles)

    def monster_at(self, tile):
        for m in self.monsters:
            if m.pos_x == tile[0] and m.pos_y == tile[1]:
                return m
        return None

    def attack_monster_at(self, tile, player, world):
        m = self.monster_at(tile)
        if m:
            m.defend(world, player)

    def get_info(self, tile):
        m = self.monster_at(tile)
        if m:
            return m.get_info()
        else:
            return ''
