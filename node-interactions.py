import operator
from os import listdir
from os.path import isfile, join
import sys

def get_dict_of_all_contacts():
    datapath = 'flu-data/moteFiles'
    datafiles = [f for f in listdir(datapath) if isfile(join(datapath,f)) ]
    dict_of_all_contacts = dict()
    for datafile in datafiles:
        node_contacts = dict()
        f = open(join(datapath,datafile), 'r')
        line = f.readline()
        while line:
            numlist = line.split()
            if len(numlist) < 5:
                continue
            node = numlist[0]
            time = int(numlist[-1])
            if node not in node_contacts:
                node_contacts[node] = time
            line = f.readline()
        nodename = datafile[5:]
        dict_of_all_contacts[nodename] = node_contacts
        f.close()
    return dict_of_all_contacts


dict_of_all_contacts = get_dict_of_all_contacts()


node1 = dict_of_all_contacts['1']


infected = {}
for k, v in node1.iteritems():
    infected[k] = v

final_infected = infected.copy()

for k,v in infected.iteritems():
    current_node = dict_of_all_contacts[k]
    for k, v in current_node.iteritems():
        if k not in infected:
            final_infected[k] = v
        else:
            if infected[k] > v:
                final_infected[k] = v

print len(final_infected)
sorted_infected = sorted(final_infected.iteritems(), key=operator.itemgetter(1))
print sorted_infected


