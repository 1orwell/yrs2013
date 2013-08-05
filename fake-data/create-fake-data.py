#This script creates fake nodes and interactions to test virus spread on



nodes = 10

for currentnode in range(1,nodes+1):
    currentfilename = "node-" + str(currentnode) + ".txt"
    currentfile =  file("moteFiles/" + currentfilename,"a")
    currentfile.write("This is node" + str(currentnode) + "\n")
    currentfile.close()


print "Finito"
