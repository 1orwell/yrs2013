'''Generate necessary dump files'''

#options
size = 790 
regenerate_graph = False
days = 1
###

import igraph, pickle, random
import math
from collections import OrderedDict


def run_day(day):

    output = './days/'+str(size)+'-'+str(day)+'.dat'

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
        pickle.dump(g,open('dump.dat','w'))
        print 'Finished'



    #take sample of n points
    sample = random.sample(range(1,788),790-size)
    g.delete_vertices(sample)
    print g.summary()


    #Fiddle layout
    
    print 'Working out layout'
    l = g.layout_kamada_kawai()
    '''
    #igraph.plot(g, layout = l)

    generating own layout now, starting everyone at their own location
    '''

    #coords definition stolen from sim_group_move.py
    coords = []

    wrap = 11 #11 positions per row, ie range(0,11) will give you 11 positions

    #must pass coords as negative
    #x must be between -5 and -3
    #y must be between -28 and -26
    #


    col_length = size/wrap

    coord_x_spacing = float(2.0/wrap)
    coord_y_spacing = float(2.0/col_length)

    for x in range(wrap):
            for y in range(col_length):
                    t = (-5 + (x*coord_x_spacing)),(-28 + (y*coord_y_spacing))
                    coords.append(t)

    
    
    def distance(x, y): return math.sqrt((x[0] - y[0])**2 +  (x[1] - y[1])**2)

    order =  sorted(enumerate(coords), key = lambda x: distance(x[1], l.centroid()))
    order = [x[0] for x in order]

    #dump coords file

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
        cs, movs = 0, 0
        for contact in f:
            cs += 1
            line = map(int, contact.split())
            contact_id = line[0]
            time = (line[-1] - mintime + 1)
            if contact_id in completed:
                movs += 1
                current_max = 0
                current_time = -1
                for t, pos in times[contact_id].items():
                    if current_time < t <= time and pos != 'free':
                        current_max = pos
                        current_time = t
                times[node][time] = current_max 
            else:
              times[node][time] = 'free' 	
        completed.append(node)
        print node, cs, movs
        f.close()

    print 'Writing movement file'
    out = {'coords': coords, 'movement': times}
    pickle.dump(out, open(output, 'w'))
    return times

def multiple_runs(days):
    for day in range(days):
        times = run_day(day)
    return times

times = multiple_runs(days)
