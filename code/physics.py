import math

#constants describing physics
wheelBase=20
track=10

#status
slip=False

def move(x,y,dir,forward,dirChange):
    if dirChange==0:
        x=x+math.sin(dir)*forward
        y=y+math.cos(dir)*forward
    else:
        rad=wheelBase/math.atan(dirChange)
        rad=math.sqrt(rad*rad+wheelBase*wheelBase/4)
        origo=(x+math.cos(dir)*rad,y-math.sin(dir)*rad)
        dir=dir+forward/rad
        x=origo[0]-math.cos(dir)*rad
        y=origo[1]+math.sin(dir)*rad
    return (x,y,dir)