import math

def distance(obj1=(0,0), obj2=(0,0)):
    return math.sqrt( (obj1[0]-obj2[0]) ** 2 + (obj1[1]-obj2[1]) ** 2 )

def can_ray_pass(x, y, world):
    if world[x][y] == 'X':
        return False
    return True

def can_see_point(x0,y0,x1,y1,world):
    wall = False
    if not can_ray_pass(x1,y1,world):
        wall = True
    wall_chain = 0
    pts = []
    swapXY = math.fabs(y1-y0) > math.fabs(x1-x0)
    tmp = 0
    if  swapXY :
        tmp = x0
        x0 = y0
        y0 = tmp
        tmp = x1
        x1 = y1
        y1 = tmp

    if  x0 > x1 :
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    deltax = x1 - x0
    deltay = math.floor(math.fabs(y1-y0))
    error = math.floor(deltax/2)
    y = y0
    ystep = 0

    if y0 < y1 :
        ystep = 1
    else:
        ystep = -1

    if swapXY :
        for x in range(x0,x1+1) :
            if not can_ray_pass(y,x, world):
                if not wall:
                    return False
                if wall_chain == -1:
                    return False
                else:
                    wall_chain += 1
            elif wall_chain > 0:
                wall_chain = -1
                
            pts.append((y,x))
            error -= deltay
            if error < 0 :
                y = y + ystep;
                error = error + deltax
    else:
        for x in range(x0,x1+1) :
            if not can_ray_pass(x,y,world):
                if not wall:
                    return False
                if wall_chain == -1:
                    return False
                else:
                    wall_chain += 1
            elif wall_chain > 0:
                wall_chain = -1
            pts.append((x,y))
            error -= deltay
            if error < 0:
                y = y + ystep
                error = error + deltax
    return True

def get_line(x0,y0,x1,y1):
    pts = []
    swapXY = math.fabs(y1-y0) > math.fabs(x1-x0)
    tmp = 0
    if  swapXY :
        tmp = x0
        x0 = y0
        y0 = tmp
        tmp = x1
        x1 = y1
        y1 = tmp
    if  x0 > x1 :
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    deltax = x1 - x0
    deltay = math.floor(math.fabs(y1-y0))
    error = math.floor(deltax/2)
    y = y0
    ystep = 0

    if y0 < y1 :
        ystep = 1
    else:
        ystep = -1

    if swapXY :
        for x in range(x0,x1+1) :
            pts.append((y,x))
            error -= deltay
            if error < 0 :
                y = y + ystep;
                error = error + deltax
    else:
        for x in range(x0,x1+1) :
            pts.append((x,y))
            error -= deltay
            if error < 0:
                y = y + ystep
                error = error + deltax
    return pts

def get_circle(x0,y0,radius):
    tiles = []
    tiles.append((x0+radius, y0))
    tiles.append((x0-radius, y0))
    tiles.append((x0, y0+radius))
    tiles.append((x0, y0-radius))
    x = 0
    y = radius
    d= 3 - 2*radius

    while x<=y :
        if d<=0:
            d+=4*x+6
        else:
            d = d+4*(x-y)+10
            y -= 1
        x+=1
        tiles.append(( x + x0,  y + y0))
        tiles.append(( y + x0,  x + y0))
        tiles.append((-x + x0,  y + y0))
        tiles.append((-y + x0,  x + y0))
        tiles.append((-x + x0, -y + y0))
        tiles.append((-y + x0, -x + y0))
        tiles.append(( x + x0, -y + y0))
        tiles.append((y + x0, -x + y0))
    return tiles

def disc_from_circle(x0, y0, radius):
    circle = get_circle(x0, y0, radius)
    to_add = []
    for point in circle:
        dx = x0-point[0]
        #si le point est a gauche, on prend toute la ligne avec une symetrie
        if dx > 0:
            for x in range(dx*2):
                to_add.append( (point[0]+x, point[1]) )

    circle.extend(to_add)
    return circle

def filter_valid(table, limit):
    return filter(lambda point: point[0] >= 0 and point[0] < limit and point[1] >= 0 and point[1] < limit, table)
    
def is_valid_move(point, world, limit):
    if point[0] >= 0 and point[0] < limit and point[1] >= 0 and point[1] < limit:
        if world.tiles[point[0]][point[1]] != 'X':
            return True
    return False
