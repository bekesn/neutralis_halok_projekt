from datetime import datetime
import pygame
import math

pygame.init()
Display = pygame.display.set_mode((900,650))
Display.fill((0,0,0))

outerReady=False
innerReady=False
startReady=False
ready= False
list1=[]
list2=[]
pygame.display.set_caption("Outer arc","b")
go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            go = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Display.fill((0, 0, 0))
            buttons = pygame.mouse.get_pressed()
            if not outerReady:
                if buttons[2]:
                    if len(list1)>0:
                        list1.pop(len(list1)-1)
                elif buttons[0]:
                    (x, y)=pygame.mouse.get_pos()
                    list1.append([x, y])
                    print(x,y)
                elif buttons[1]:
                    outerReady=True
                    pygame.display.set_caption("Inner arc")
            elif not innerReady:
                if buttons[2]:
                    if len(list2)==0:
                        pygame.display.set_caption("Outer arc")
                        outerReady=False
                    else:
                        list2.pop(len(list2) - 1)
                elif buttons[0]:
                    (x, y)=pygame.mouse.get_pos()
                    list2.append([x, y])
                    print(x,y)
                elif buttons[1]:
                    pygame.display.set_caption("Start")
                    innerReady = True
            elif not startReady:
                if buttons[2]:
                    pygame.display.set_caption("Inner arc")
                    innerReady = False
                elif buttons[0]:
                    start = pygame.mouse.get_pos()
                    startReady = True
                    pygame.display.set_caption("Start direction")
            else:
                if buttons[2]:
                    if ready:
                        ready = False
                        pygame.display.set_caption("Start direction")
                    else:
                        pygame.display.set_caption("Start")
                        startReady = False
                elif buttons[0] and not ready:
                    pos = pygame.mouse.get_pos()
                    pos = [pos[0]-start[0], pos[1]-start[1]]
                    if pos[1]==0:
                        pass
                    else:
                        startDir=-math.pi/2
                        startDir=math.atan(float(pos[0])/float(pos[1]))
                        if pos[1] < 0:
                            startDir= startDir+math.pi
                        print(startDir)
                        ready = True
                        pygame.display.set_caption("Ready to save")
                elif buttons[1] and ready:
                    now = datetime.now()
                    # Choose between the train and test folders
                    #f = open("train/tracks_" + now.strftime("%m%d_%H%M%S") + ".txt", "x")
                    f = open("test/tracks_" + now.strftime("%m%d_%H%M%S") + ".txt", "x")
                    for i in list1:
                        f.write(str(i[0])+","+str(i[1])+",\n")
                    f.write("---\n")
                    for i in list2:
                        f.write(str(i[0]) + "," + str(i[1]) + ",\n")
                    f.write("---\n")
                    f.write(str(start[0])+","+str(start[1])+",\n")
                    f.write("---\n")
                    f.write(str(startDir) + ",\n")
                    f.close()
                    pygame.quit()
                    go=False
            if go:
                if len(list1) > 1:  pygame.draw.polygon(Display, (255, 0, 0), list1, 3)
                if len(list2) > 1:  pygame.draw.polygon(Display, (255, 0, 0), list2, 3)
                if ready: pygame.draw.line(Display, (0, 128, 255), start,
                                       (start[0]+20*math.sin(startDir), start[1]+20*math.cos(startDir)), 3)
                if startReady: pygame.draw.circle(Display, (0, 0, 255), start, 3)
                pygame.display.update()
