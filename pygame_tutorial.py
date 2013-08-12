import pygame, sys
from classes import *

pygame.init()
width, height = 640, 360
screen = pygame.display.set_mode((width, height),0, 32)
clock = pygame.time.Clock()
FPS = 24 #24 frames per second

bug = Bug(0, 100, 40, 40, "images/bug.png")

#while loop allows black screen to stay open and close properly
while True:
    #PROCESSES
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #PROCESSES
    #LOGIC
    #LOGIC
    #DRAW

    screen.fill((0,0,0))
    BaseClass.allsprites.draw(screen)
    pygame.display.flip() #makes sure everything is drawn on screen
    #DRAW

    bug.motion()
    clock.tick(FPS) # sets clock tick (frames per second) to 24

