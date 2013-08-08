import igraph, pickle, random
import math
from collections import OrderedDict

size = 50

g = pickle.load(open('dump.dat'))


g.delete_edges(weight_gt=1/180.0)

#take sample of n points
sample = random.sample(range(1,788),790-size)
g.delete_vertices(sample)
print g.summary()


#Fiddle layout
print 'Working out layout'
l = g.layout_kamada_kawai()
igraph.plot(g, layout = l)



