import pickle
import math
import pygame, sys, random, os

#options

width, height = 1000, 800

#

def changeCoords(cs):
    x, y = cs
    return ((x * (width*0.8)+50) , (y* (height*0.8)+50) )

def normalise(cs):
    smallest_x = min([x[0] for x in cs  ])
    smallest_y = min([x[1] for x in cs ])
    print smallest_x, smallest_y
    # make all positive
    cs = [[x[0] - smallest_x, x[1] - smallest_y] for x in cs]
    #normalise
    biggest_x = max((x[0] for x in cs), key=abs)
    biggest_y = max((x[1] for x in cs), key=abs)
    cs = [[x[0]/float(biggest_x), x[1]/float(biggest_y)] for x in cs]
    #sanity check
    print  max((x[0] for x in cs), key=abs), max((x[1] for x in cs), key=abs)
    return cs

def display(fin):
        fin = os.path.join('data', fin)
        f = open(fin)
        data = pickle.load(f)
 

        coords = data['coords']
        mvs = data['moves']
        virus = data['virus']
        
        #load sprites
        green = pygame.image.load("images/green.png")
        green = pygame.transform.scale(green, (5,5))
        red = pygame.image.load("images/red.png")
        red = pygame.transform.scale(red, (5,5))

        pygame.init()
        screen = pygame.display.set_mode((width, height),0, 32)

        coords = normalise(coords)
        coords = map(changeCoords, coords)
        targets = coords[:]
        clock = pygame.time.Clock()
        FPS = 24 #24 frames per second
        i = 0
        node_dict = {}
        FPC = 2



        health_clr = (56, 48, 225)
        infec_clr = (225, 54, 100)

        people = []
        num_of_nodes = len(coords)

        screen.fill((225,225,225))
        for i in range(num_of_nodes):
            x, y = coords[i]
            people.append(screen.blit(green, (x,y)))

        time =1
        #while loop allows black screen to stay open and close properly
        while True:
            #PROCESSES
            if time % FPC == FPC-1:
                print virus[time/FPC]
                print mvs[time/FPC]
                print time/FPC
                if time/FPC in mvs:
                    #move required people for that tick
                    for person, move in mvs[time/FPC]:
                        x,y = coords[move-1]
                        x = x + random.randint(0,5)-2
                        y = y + random.randint(0,5)-2
                        targets[person-1] = [x,y]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            

            #draw objects
            screen.fill((255,255,255))
            for i, o in enumerate(people[::]):
                #calculate the next position
                x,y = o.x, o.y
                target_x, target_y = tuple(targets[i])
                targetVector_x, targetVector_y = ((target_x - x)/FPC, (target_y - y)/FPC)
                rand_int = 0
                #rand_int = random.randint(0,4)
                if i-1 not in virus[time/FPC]:
                    people.append(screen.blit(green, (x+ targetVector_x + rand_int, y + targetVector_y + rand_int)))
                else:
                    people.append(screen.blit(red, (x+ targetVector_x + rand_int, y + targetVector_y)))
            
            #purge queue
            people = people[num_of_nodes:]

            time += 1
            pygame.display.flip() #makes sure everything is drawn on screen

            clock.tick(FPS) # sets clock tick (frames per second) to 24


if __name__ == '__main__':
  display('virus.dat')
