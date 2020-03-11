import physics
import kirajzolas
import perception

x=300.0
y=300.0
dir=0.3
kirajzolas.palya_1k, kirajzolas.palya_1b = kirajzolas.getTracks()
print(kirajzolas.palya_1k)
print(kirajzolas.palya_1b)
while True:
    (x,y,dir)=physics.move(x,y,dir,0.3,0.3)
    perception.calcDistances(x,y,dir)
    kirajzolas.drawPalya(x,y,dir)

