import pygame, sys

pygame.init()
screen = pygame.display.set_mode((640, 360), 0, 32)

clr1 = (22, 122, 211)
clr2 = (0, 44, 166)
clr3 = (34, 55, 245)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



pygame.draw.line(screen, clr2, (0 , 0), (640 , 360), 5)
pygame.draw.rect(screen, clr3, (40, 40, 360, 360))

pygame.display.flip()

