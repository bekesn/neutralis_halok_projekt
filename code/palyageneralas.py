import pygame
import sys

pygame.init()
Display = pygame.display.set_mode((900,900))
Display.fill((0,0,0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons=pygame.mouse.get_pressed()
            if buttons[1]:
                pass
            elif buttons[0]:
                (x,y)=pygame.mouse.get_pos()
                print(x,y)