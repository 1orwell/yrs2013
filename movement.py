import pygame, sys

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height),0, 32)

health_clr = (56, 48, 225)

clock = pygame.time.Clock()
FPS = 1

time = 0
x = 20
y = 20

#while loop allows black screen to stay open and close properly
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((225,225,225))

    for i in range(100):
        circle = pygame.draw.circle(screen, health_clr, (x, y),10)
        time += 1
        if time % 10 == 0:
            screen.fill((225,225,225))
            x += 2
            y += 2
            circle

    pygame.display.flip() #makes sure everything is drawn on screen
    #DRAW

    clock.tick(FPS)
