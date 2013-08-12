import igraph, pickle
import math

g = igraph.Graph()
g.add_vertices(790)
g.es["weight"] = 1.0
g.delete_vertices([0])
print g.is_weighted()

#with open('/home/elise/projects/yrs2013/flu-data/edgeLists/durationCondition/addThenChop/dropoff=0/minimumDuration=1/deltaT=1620/staticWeightedEdgeList_at=1350_min=540_max=2159.txt') as edges:
 #   for edge in edges:
  #      u, v, w = map(int, edge.split())
   #     g[u, v] = 1/w

g = pickle.load(open('dump.dat'))
g.delete_vertices(g.vs(_degree_eq = 0))

l = g.layout_kamada_kawai()
igraph.plot(g, layout = l)

def distance(x, y):
    diff_in_x = x[0] - x[1]
    diff_in_y = y[0] - y[1]
    distance = math.sqrt((diff_in_x**2) + (diff_in_y**2))
    return distance

centre_coords  = l.centroid()
coords = l.coords
def dist_from_centre(centre_cords, coords, distance):
    node_coords = list(enumerate(l.coords()))
    distances = {}
    for current_node, coords in node_coords:
        distance_from_centre = dinstance(l.centroid(), coords)
        distances[current_node] = distance_from_centre
    return distances

order =  sorted(enumerate(l.coords), key = lambda x: distance(x[1], l.centroid()))
print order[:5]
order = [x[0] for x in order]


completed = []
times = {}

for node in order:
    if node == 0: continue
    print node
    times[node] = {0: node}
    node_name  = 'node-'+str(node)
    f = open('moteFiles/'+node_name, 'r')
    for contact in f:
        line = contact.split()
        contact_id = int(line[0])
        time = int(line[-2])
        if contact_id in completed:
            current_max = 0
            current_time = -1
            for t, pos in times[contact_id].items():
                if current_time < t <= time:
                    current_max = pos
                    current_time = t
            position = current_max
            times[node][time] = position
        else:
            continue
    completed.append(node)
    f.close()



