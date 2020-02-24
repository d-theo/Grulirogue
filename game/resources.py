import pyglet

def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image('player25.png')
gobelin_image = pyglet.resource.image('gobelin.png')
archer_image = pyglet.resource.image('archer.png')

tile_grey = pyglet.resource.image('tile-grey.png')
tile_black = pyglet.resource.image('tile-black.png')
tile_blue = pyglet.resource.image('tile-blue.png')
stair = pyglet.resource.image('stair.png')

crossbow_image = pyglet.resource.image('crossbow_s.png')
bow_image = pyglet.resource.image('bow.png')
arrow_image = pyglet.resource.image('arrow.png')
bullet_image = pyglet.resource.image('bullet.png')
bolt_image = pyglet.resource.image('bolt.png')
arquebuse_image = pyglet.resource.image("arquebuse_s.png")

bolt_shot_image = pyglet.resource.image("bolt_shot.png")
arrow_shot_image = pyglet.resource.image("arrow_shot.png")

blood_image = pyglet.resource.image('blood.png')
health_image = pyglet.resource.image('health.png')
min_lif_ring_img = pyglet.resource.image('min_lif_ring.png')
min_dex_ring_img = pyglet.resource.image('min_dex_ring.png')
min_amr_ring_img = pyglet.resource.image('min_amr_ring.png')
min_atk_ring_img = pyglet.resource.image('min_atk_ring.png')

center_image(bolt_shot_image)
center_image(arrow_shot_image)
