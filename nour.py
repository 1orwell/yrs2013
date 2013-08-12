import pygame

pygame.init()
screen = pygame.display.set_mode((640, 360),0 ,32)

ctr1 = (22, 122, 211)
ctr2 = (0, 44, 166)
ctr3 = (34, 55, 245)
while true:
    for event in pygame.event.get():
        pygame.quit()
        sys.exit()

pygame.draw.rect(screen, ctr3, (40, 40, 300, 45))
pygame.draw.circle(screen, ctr2, (350, 200) , 80, 40)

pygame.display.flip()
