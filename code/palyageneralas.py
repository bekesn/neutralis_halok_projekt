import pygame
import sys
from datetime import datetime

pygame.init()
Display = pygame.display.set_mode((900,900))
Display.fill((0,0,0))

bool1=False
list1=[]
list2=[]
pygame.display.set_caption("Külsö iv","b")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Display.fill((0, 0, 0))
            buttons = pygame.mouse.get_pressed()
            if not bool1:
                if buttons[2]:
                    if len(list1)>0:
                        list1.pop(len(list1)-1)
                elif buttons[0]:
                    (x, y)=pygame.mouse.get_pos()
                    list1.append([x, y])
                    print(x,y)
                elif buttons[1]:
                    bool1=True
                    pygame.display.set_caption("Belsö iv", "b")
            else:
                if buttons[2]:
                    if len(list2)==0:
                        pygame.display.set_caption("Külsö iv", "b")
                        bool1=False
                    else:
                        list2.pop(len(list1) - 1)
                elif buttons[0]:
                    (x, y)=pygame.mouse.get_pos()
                    list2.append([x, y])
                    print(x,y)
                elif buttons[1]:
                    now = datetime.now()
                    f=open("pontok/pontok_"+now.strftime("%m%d_%H%M%S")+".txt","x")
                    for i in list1:
                        f.write(str(i[0])+","+str(i[1])+",\n")
                    f.write("---\n")
                    for i in list2:
                        f.write(str(i[0]) + "," + str(i[1]) + ",\n")
                    f.close()
                    pygame.quit()
                    sys.exit()
            if len(list1) > 1:  pygame.draw.polygon(Display, (255, 0, 0), list1, 3)
            if len(list2) > 1:  pygame.draw.polygon(Display, (255, 0, 0), list2, 3)
            pygame.display.update()
