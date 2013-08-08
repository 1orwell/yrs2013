import pickle
import pygame, sys

#f = open('movement-50.dat')
f = open('virus.dat')

data = pickle.load(f)

coords = data['coords']
mvs = data['moves']
virus = data['virus']

pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height),0, 32)

clock = pygame.time.Clock()
FPS = 24 #24 frames per second
i = 0
node_dict = {}

health_clr = (56, 48, 225)
infec_clr = (225, 54, 100)

num_of_nodes = len(coords)
time = 0

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


    def time_changes():
        pass


    for i in range(num_of_nodes):
        x, y = coords[i - 1]
        x = int((x*100) + (width/2))
        y = int((y*100) + (height/2))
        circle = pygame.draw.circle(screen, health_clr, (x, y),10)#(x,y), radius, hollow
        circle
        i += 1
        print time
        if time > 900:
            screen.fill((225,225,225))


    time += 1

    pygame.display.flip() #makes sure everything is drawn on screen
    #DRAW

    clock.tick(FPS) # sets clock tick (frames per second) to 24

