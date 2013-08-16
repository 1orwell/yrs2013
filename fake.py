'''Generate necessary dump files'''

#options
size = 100
regenerate_graph = False
days = 1
force_layout = False 
default = str(size)+'.dat'

###

import igraph, pickle, random, os
import math
from collections import OrderedDict

def process(fout):

    output = os.path.join('data',fout)

    try:
        #load graph if previously generated.
        g = pickle.load(open('dump.dat'))
        print 'Graph loaded from dump.dat'
    except IOError:
        #generate graph if it does not exist in the directory
        print 'Generating graph to dump.dat'
        g = igraph.Graph()
        g.add_vertices(791)
        g.es["weight"] = 1.0
        g.delete_vertices([0])
        with open('./flu-data/edgeLists/durationCondition/addThenChop/dropoff=0/minimumDuration=1/deltaT=1620/staticWeightedEdgeList_at=1350_min=540_max=2159.txt') as edges:
            for edge in edges:
                u, v, w = map(int, edge.split())
                g[u, v] = 1.0/w
        g.delete_vertices(g.vs(_degree_eq = 0))
        pickle.dump(g,open('dump.dat','wb'))
        print 'Finished'



    #take sample of n points
    sample = random.sample(range(1,788),790-size)
    g.delete_vertices(sample)
    print g.summary()

    
    #Fiddle layout
    print 'Working out layout'
    if force_layout: 
    
      #starting everyone at their own location


      #coords definition stolen from sim_group_move.py
      coords = []

      wrap = 10 #positions per row

      col_length = int(math.ceil(size/wrap))

      for y in range(col_length):
        for x in range(wrap):
          coords.append((x,y))
      print coords
      centre = (wrap/2, col_length/2)

    
    else: 
      l = g.layout_kamada_kawai()
      centre = l.centroid()
      coords = l.coords

    def distance(x, y): return math.sqrt((x[0] - y[0])**2 +  (x[1] - y[1])**2)
      
    #sort the coords by their position from the centre
    order =  sorted(enumerate(coords), key = lambda x: distance(x[1], centre))
    order = [x[0] for x in order]



    #work out mininum global time
    mintime = 1000 #must be less than this
    for x in order:
            if x == 0: continue
            with open('./flu-data/moteFiles/node-'+str(x)) as fin:
                    line = fin.readline()
                    if line:
                            t = int(line.split()[-1])
                            if t < mintime:
                                    mintime = t


    completed = []
    times = {}
    print 'Generating movement file'
    for node in order:
        if node == 0: continue
        times[node] = OrderedDict({0 : node})
        node_name  = 'node-'+str(node)
        f = open('./flu-data/moteFiles/'+node_name, 'r')
        for contact in f:
            line = map(int, contact.split())
            contact_id = line[0]
            time = (line[-1] - mintime + 1)
            if contact_id in completed:
                current_max = 0
                current_time = -1
                for t, pos in times[contact_id].items():
                    if current_time < t <= time:
                        current_max = pos
                        current_time = t
                position = current_max
                times[node][time] = position
	
        completed.append(node)
        f.close()

    print 'Writing movement file'
    out = {'coords': coords, 'movement': times}
    pickle.dump(out, open(output, 'wb'))

if __name__ == '__main__':
  process(default)
