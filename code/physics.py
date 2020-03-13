import math

#constants describing physics
wheelBase=20
track=10
slipEnabled=True
slipLimit=0.004
turnLimit=0.5

#status
slip=False
collision=False

def move(x,y,dir,forward,dirChange):
    if dirChange==0:
        x=x+math.sin(dir)*forward
        y=y+math.cos(dir)*forward
    else:
        dirChange = min(dirChange, turnLimit)
        dirChange = max(dirChange, -turnLimit)
        rad=wheelBase/math.atan(dirChange)
        rad=math.sqrt(rad*rad+wheelBase*wheelBase/4)*dirChange/abs(dirChange)
        origo=(x+math.cos(dir)*rad,y-math.sin(dir)*rad)
        if slipEnabled and abs(forward * forward / rad) > slipLimit:
            slip = True
            x = x + math.sin(dir) * forward
            y = y + math.cos(dir) * forward
            dir=dir+forward/rad/3
        else:
            slip=False
            dir=dir+forward/rad
            x=origo[0]-math.cos(dir)*rad
            y=origo[1]+math.sin(dir)*rad
    return (x,y,dir)