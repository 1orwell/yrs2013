import pickle
import pygame, sys

#f = open('movement-50.dat')
f = open('virus.dat')

data = pickle.load(f)

green = pygame.image.load("images/green.png")
red = pygame.image.load("images/red.png")

def changeCoords(cs):
    x, y = cs
    return ((x * width) , (y* height) )

def normalise(cs):
    smallest_x = min(x[0] for x in cs if x[0] < 0)
    smallest_y = min(x[1] for x in cs if x[0] < 0)
    # make all positive
    cs = [[x[0] + smallest_x, x[1] + smallest_y] for x in cs]
    #normalise
    biggest_x = max((x[0] for x in cs), key=abs)
    biggest_y = max((x[1] for x in cs), key=abs)
    cs = [[x[0]/biggest_x, x[1]/biggest_y] for x in cs]
    #sanity check
    print  max((x[0] for x in cs), key=abs), max((x[1] for x in cs), key=abs)
    return cs

pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height),0, 32)


coords = data['coords']
mvs = data['moves']
virus = data['virus']

coords = normalise(coords)
coords = map(changeCoords, coords)
targets = coords[:]
clock = pygame.time.Clock()
FPS = 24 #24 frames per second
i = 0
node_dict = {}
FPC = 6



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
    if time % FPC == FPC-1:
        print virus[time/FPC]
        print mvs[time/FPC]
        print time/FPC
        if time/FPC in mvs:
            for person, move in mvs[time/FPC]:
                targets[person-1] = coords[move-1]
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
        targetVector_x, targetVector_y = ((target_x - x)/FPC, (target_y - y)/FPC)
        if i-1 not in virus[time/FPC]:
            people.append(screen.blit(green, (x+ targetVector_x, y + targetVector_y)))
        else:
            people.append(screen.blit(red, (x+ targetVector_x, y + targetVector_y)))

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

