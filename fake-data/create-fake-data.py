#This script creates fake nodes and interactions to test virus spread on

import random

nodes = 10



#move through time
for tick in range(0,30):
    print "Tick is ", tick
    interactions = {}
    for node in range(1,(nodes+1)):
        interactions[node] = []
    print interactions
    #look at nodes in turn
    for nodeA in range(1,(nodes+1)):
        print "Node A is " + str(nodeA)
        for nodeB in range(1,(nodes+1)):
            #see if node interacts
            interaction = random.randint(0,4)
            #if node interacts
            if interaction == 1:

                if nodeB not in interactions[nodeA]:
                    if nodeB != nodeA:
                        #mark node as interacted with for this tick
                        interactions[nodeA].append(nodeB)
                        interactions[nodeB].append(nodeA)

                        #create/access files 
                        fileAname = "node-" + str(nodeA) + ".txt"
                        fileA =  file("moteFiles/" + fileAname,"a")
                        fileBname = "node-" + str(nodeB) + ".txt"
                        fileB =  file("moteFiles/" + fileBname,"a")
                        

                        #generate random sequence and strength
                        sequence = str(random.randint(1,nodes))
                        strength = "230"
                        time = str(tick)
                        #write interaction to files
                        fileA.write(str(nodeB) + " " + sequence + " " + strength + " " + sequence + " " + time + "\n")
                        fileB.write(str(nodeA) + " " + sequence + " " + strength + " " + sequence + " " + time + "\n")
                        
                    
                
                        fileA.close()
                        fileB.close()

    
