from pyglet import image

SIZE = 50

maping = {
    (255,255,255):'0',    #empty
    (0,0,0):'X',          #wall
    (255,0,0):'e',        #ennemy
    (255,100,0):'e1',        #ennemy
    (0,255,255):'w',      #weapon
    (0,255,0):'i',        #initial
    (255,255,0):'f',      #final
    (255,0,255):'l',      #item
}

def generate_map(path):
    pic = image.load(path)
    mapImage = pic.get_image_data()

    tiles = [[0 for x in range(SIZE)] for x in range(SIZE)] 
    level = [[0 for x in range(SIZE)] for x in range(SIZE)] 

    for x in range(SIZE):
        for y in range(SIZE):
            pix = mapImage.get_region(x,y,1,1).get_image_data().get_data("RGB", 3)
            tiles[x][y] = (ord(pix[0]),ord(pix[1]),ord(pix[2]))

    for x in range(SIZE):
        for y in range(SIZE):
            level[x][y] = maping[tiles[x][y]]

    return level
