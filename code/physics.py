import math

# constants describing physics
wheelBase = 20
track = 10
slipEnabled = False
slipLimit = 0.004
turnLimit = 0.3   # math.pi/4
g = 9.81
mu = 0.8  # Tapadási súrlódási tényező
px = 5  # px/s to m/s
pr = 10  # m to px
rand=10
skid_factor=5 # Megadja, mennyivel változzon a csúszás értéke
max_accelerating=0.05

# status
slip = False
collision = False
skid=0.0
speed=0.0

def reset():
    global slip
    global collision
    global skid
    global speed
    slip = False
    collision=False
    skid=0.0
    speed=0.0


def move(x, y, dir, speedChange, dirChange):
    global skid # így lehet elérni őket függvényben
    global slip
    global speed
    speed = speed+speedChange  # jelenlegi sebesség
    if dirChange == 0:
        x = x + math.sin(dir) * speed
        y = y + math.cos(dir) * speed
        skid = 0.0  # Ebben az esetben nem csúszik az autó
    else:
        dirChange = min(dirChange, turnLimit)
        dirChange = max(dirChange, -turnLimit)
        rad = wheelBase / math.tan(dirChange)
        rad = math.sqrt(rad * rad + wheelBase * wheelBase / 4) * dirChange / abs(dirChange)
        origo = (x + math.cos(dir) * rad, y - math.sin(dir) * rad)
        v_max = math.sqrt(g * mu * abs(rad / pr))
        rad_min = speed * speed * px * px * pr / (g * mu)
        if slipEnabled and speed * px > v_max:
            slip = True
            if abs(rad) + skid < rad_min:   # Addig növeljük a csúszás értékét, amíg a megfelelő körpályára kerül
                mrad = rad / (abs(rad) + skid)
            else:
                mrad = rad / rad_min
                skid = rad_min - abs(rad) + 10  # Amint a megfelelő körpályán vagyunk, nem változik az értéke. 10 := biztonsági tényező
            # print(forward, v_max, rad, rad_min, skid, mrad)
            x = x + math.sin(dir) * speed
            y = y + math.cos(dir) * speed
            dir = dir + speed / rad * abs(mrad)   # Ezzel a képlettel adjuk meg a csúszás mértékét
        else:
            slip = False
            skid = 0.0  # Ebben az esetben nem csúszik az autó
            dir = dir + speed / rad
            x = origo[0] - math.cos(dir) * rad
            y = origo[1] + math.sin(dir) * rad
    skid = skid + speed * skid_factor  # Csúszás értékének meghatározása a sebesség függvényében
    return (x, y, dir, skid)
