import pyglet
import resources
import physicalobject
import player
import maps
import monster
import mapmonster
import mapitem
import item
import mapcreator
from bullets_controller import BulletsController
from blood_controller import BloodController

from pyglet.window import mouse

def remove_tuto(dt):
    global tuto
    tuto.pop()

def add_shot_tuto(dt):
    global tuto
    global tuto_how_shot
    tuto.append(tuto_how_shot)

def add_pick_tuto(dt=0):
    global tuto
    global tuto_how_item
    global tuto_pick_enabled
    if len(tuto) > 0:
        pyglet.clock.schedule_once(add_pick_tuto, 2)
    else:
        tuto.append(tuto_how_item)
        pyglet.clock.schedule_once(remove_tuto, 3)
        tuto_pick_enabled = False

#debug
fps_display = pyglet.clock.ClockDisplay()

#globals
score   = 0
log     = "Nouvelle partie"
overlay = None
shake   = 10
level   = 1

#tuto
tuto = []
tuto_how_move = pyglet.text.Label("Use arrows to move",x=400,y=300, anchor_x="center", anchor_y="center")
tuto_how_shot = pyglet.text.Label("Use left click to shot and reload",x=400,y=300, anchor_x="center", anchor_y="center")
tuto_how_item = pyglet.text.Label("Use T to pick an item, I to open inventory",x=400,y=300, anchor_x="center", anchor_y="center")
tuto_pick_enabled = True

tuto.append(tuto_how_move)
pyglet.clock.schedule_once(remove_tuto, 3)
pyglet.clock.schedule_once(add_shot_tuto, 4)
pyglet.clock.schedule_once(remove_tuto, 7)

game_window = pyglet.window.Window(800, 600)
main_batch  = pyglet.graphics.Batch()
map_batch   = pyglet.graphics.Batch()

selected_tile = None
log_label = None
hero = None
the_map = None
all_monsters = None
bullets_controller = BulletsController()
blood_controller = BloodController()
life_label = None
weapon_label = None
level_label = None

should_add_handlers = False

def init_level(next_level):
    global selected_tile, log_label, hero, the_map, all_monsters, life_label, weapon_label, level_label, bullets_controller, blood_controller, should_add_handlers, level, map_batch, main_batch
    main_batch  = pyglet.graphics.Batch()
    map_batch   = pyglet.graphics.Batch()
    level = next_level
    current_level = mapcreator.generate_map("../maps/level"+str(level)+".png")
    selected_tile = (0,0)
    log_label = pyglet.text.Label(text=log,x=10,y=585, batch=main_batch)
    if not hero:
        hero = player.Player(batch=main_batch)
    else:
        hero.batch = main_batch
    the_map     = maps.Map(hero, current_level, level, map_batch)
    hero.x      = the_map.center[0]
    hero.y      = the_map.center[1]
    all_monsters= mapmonster.MapMonster(the_map)

    life_label  = pyglet.text.Label(color=(255,255,0,255), x=10,y=20, batch=main_batch, multiline=True, width=200)
    life_label.text = 'Health ' + str(hero.lif) + '%'

    weapon_label= pyglet.text.Label(color=(255,255,0,255), x=790, y=10, batch=main_batch, anchor_x="right")
    weapon_label.text = 'Weapon 1 : Bow(2-10) 5/5'

    level_label = pyglet.text.Label(x=790, y=585, anchor_x="right",text="Floor "+str(level), batch=main_batch)

    bullets_controller.clear_bullets()
    blood_controller.clear()
    game_window.push_handlers(the_map)
    game_window.push_handlers(the_map.key_handler)
    should_add_handlers = False

init_level(1)

@game_window.event
def on_draw():
    global should_add_handlers
    global shake
    game_window.clear()

    pyglet.gl.glLoadIdentity()
    pyglet.gl.glTranslatef(-shake, -shake, 0.0)

    map_batch.draw()
    all_monsters.draw()
    the_map.drawItems()
    bullets_controller.draw()
    main_batch.draw()

    if the_map.overlay:
        handle_overlay()
    else:
        handle_add_handlers()

    if shake > 0:
        shake -= 5

    for t in tuto:
        t.draw()

    fps_display.draw()

def handle_add_handlers():
    global should_add_handlers
    if should_add_handlers:
        game_window.pop_handlers()
        game_window.push_handlers(the_map)
        game_window.push_handlers(the_map.key_handler)
        should_add_handlers = False

def handle_overlay():
    global should_add_handlers
    if not should_add_handlers:
        should_add_handlers = True
        game_window.remove_handlers(the_map)
        game_window.remove_handlers(the_map.key_handler)
        game_window.push_handlers(the_map.overlay)

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glColor4f(0,0,0,0.8)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, 0, 600, 800, 600, 800, 0)))
    the_map.overlay.draw()


@game_window.event
def on_mouse_motion(x, y, button, modifiers):
    selected_tile = (x/maps.TILE_SIZE + the_map.scroll_x, y/maps.TILE_SIZE + the_map.scroll_y)
    new_log = the_map.all_items.get_info(selected_tile[0], selected_tile[1])
    if new_log == '':
        new_log = all_monsters.get_info(selected_tile)
    if new_log != '':
        the_map.infos = new_log

@game_window.event
def on_mouse_release(x, y, button, modifiers):
    global shake

    if the_map.is_on_cd():
        return

    can_fire = False
    clicked_tile = (x/maps.TILE_SIZE + the_map.scroll_x, y/maps.TILE_SIZE + the_map.scroll_y)
    monster = all_monsters.monster_at(clicked_tile)
    if hero.selected.count != 0:
        can_fire = True
    else:
        if hero.reload_weapon():
            the_map.set_player_turn(False)

    if monster and can_fire:
        the_map.set_player_moved(False)
        shake = hero.selected.shake
        all_monsters.attack_monster_at(clicked_tile, hero, the_map)
        hero.selected.count -= 1
        the_map.set_player_turn(False)

def update(dt):
    if the_map.go_next_level:
        the_map.go_next_level = False
        init_level(level+1)
    if the_map.overlay:
        the_map.overlay.update(dt)
        return

    the_map.update(dt)
    bullets_controller.update(dt)
    blood_controller.update(dt, the_map)

    bullets = all_monsters.getbullets()
    blood = all_monsters.getblood(map_batch)
    loot = all_monsters.getloot()

    bullets_controller.add_bullets(bullets)
    blood_controller.add_bloods(blood)
    the_map.all_items.add_items(loot)
    if loot and  tuto_pick_enabled:
        add_pick_tuto()
    all_monsters.update(dt)

    if not the_map.player_turn and the_map.cooldown == 1 :
        #resolve IA and game actions
        all_monsters.actions(hero)
        the_map.set_player_turn(True)

    log_label.text  = the_map.infos
    life_label.text = 'Health ' + str(hero.lif) + '%' + '\n' + 'Level ' + str(hero.level) + ' (' + str(hero.get_xp()) + '%)' 
    weapon_label.text = hero.weapon_log()[0]
    weapon_label.color = hero.weapon_log()[1]

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()

