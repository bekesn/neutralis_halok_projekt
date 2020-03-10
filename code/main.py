import physics
import kirajzolas
import perception

x=300.0
y=300.0
dir=0.3
while True:
    (x,y,dir)=physics.move(x,y,dir,0.1,0.8)
    perception.calcDistances(x,y,dir)
    kirajzolas.drawPalya(x,y,dir)

