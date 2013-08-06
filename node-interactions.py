import operator
from os import listdir
from os.path import isfile, join
import sys
import time

#this function outputs a dictionary with key as node, and value as another dictionary of with key as other node interacted with and value as time interacted with
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
            if time not in node_contacts:
                node_contacts[time] = [node]
            else:
                node_contacts[time].append(node)
            line = f.readline()
        nodename = datafile[5:]
        #this line strips the .txt from the file
        nodename = filter(type(nodename).isdigit, nodename)
        dict_of_all_contacts[nodename] = node_contacts
        f.close()
    return dict_of_all_contacts


def calculateMaxTime(contact_dict):
    maxtime = 0
    for node in contact_dict:
        for time in contact_dict[node]:
            if time > maxtime:
                maxtime = time
    return maxtime


dict_of_all_contacts = get_dict_of_all_contacts()
maxtime = calculateMaxTime(dict_of_all_contacts)

for tick in range(0,maxtime+1):
    print "Tick",tick
    
    for node in dict_of_all_contacts:
        time_dict = dict_of_all_contacts[node]
        if tick in time_dict:
            interactions = time_dict[tick]
        else:
            interactions="nothing"
        if interactions != "nothing":
            print "Node",node,"interacts with",interactions


'''
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
'''

