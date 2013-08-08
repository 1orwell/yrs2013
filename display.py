import pickle
import pygame, sys

#f = open('movement-50.dat')
f = open('virus.dat')

data = pickle.load(f)

green = pygame.image.load("images/green.png")

def changeCoords(cs):
    x, y = cs
    return ((x * 100) + width/2, (y* 100) + height /8)


pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height),0, 32)


coords = data['coords']
mvs = data['moves']
virus = data['virus']

coords = map(changeCoords, coords)
targets = coords[:]
clock = pygame.time.Clock()
FPS = 24 #24 frames per second
i = 0
node_dict = {}



health_clr = (56, 48, 225)
infec_clr = (225, 54, 100)

people = []
num_of_nodes = len(coords)

screen.fill((225,225,225))
for i in range(num_of_nodes):
    x, y = coords[i]
    people.append(screen.blit(green, (x,y)))

time =1
#print ('time =' time)
#while loop allows black screen to stay open and close properly
while True:
    #PROCESSES
    if time % FPS == 23:
        if time in mvs:
            for person, move in mvs[time]:
                targets[person-1] = coords[move-1]
    print pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #PROCESSES
    #LOGIC
    #LOGIC
    #DRAW
    screen.fill((255,255,255))
    for i, o in enumerate(people[::]):
        x,y = o.x, o.y
        target_x, target_y = tuple(targets[i])
        targetVector_x, targetVector_y = ((target_x - x)/FPS, (target_y - y)/FPS)
        people.append(screen.blit(green, (x+ targetVector_x, y + targetVector_y)))
    people = people[num_of_nodes:]

    def moves():
        pass


        #print time
        #if time > 900:
        #    screen.fill((225,225,225))


    time += 1
    pygame.display.flip() #makes sure everything is drawn on screen
    #DRAW

    clock.tick(FPS) # sets clock tick (frames per second) to 24

