import pickle
import pygame, sys
from test import *

f = open('flu-data/movement.dat')
mv = pickle.load(f)

pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height),0, 32)
postimedict = {}
posdict = {}

clock = pygame.time.Clock()
FPS = 1#24 frames per second
i = 0
x = 10
y = 10

clr1 = (22,122,211) #RGB
clr2 = (255,44,166)
clr3 = (34,55,245)
node = Bug(x, y, 20, 20, "images/bug.png")

num_of_nodes = len(mv.keys())

def position():
    for i in range(num_of_nodes):
        postimedict[i+1] = mv.values()[i]
        posdict[i+1] = mv.values()[i].values()



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
    screen.fill((225,225,225))

    while i in range(num_of_nodes):
        circle = pygame.draw.circle(screen, clr1, (x,y),10)#(x,y), radius, hollow
        circle
        if  width-20 < x < width+20:
            x = 10
            y += 30
        else:
            x += 25

        i = i + 1
        #circle.motion()



    pygame.display.flip() #makes sure everything is drawn on screen
    #DRAW

    clock.tick(FPS) # sets clock tick (frames per second) to 24

