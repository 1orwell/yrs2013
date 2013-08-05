#this module handles interactions between nodes to be used in the virus-spread.py module

import operator
from os import listdir
from os.path import isfile, join
import sys
import time

#this function outputs a dictionary with key as node, and value as another dictionary with key as other node in interaction and value as time interacted with
def get_dict_of_all_contacts(datapath):
    #datapath = 'flu-data/moteFiles'
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

#this function calculates the maximum time in the simulation
#used to know when to stop iterating
def calculateMaxTime(contact_dict):
    maxtime = 0
    for node in contact_dict:
        for time in contact_dict[node]:
            if time > maxtime:
                maxtime = time
    return maxtime




#below is the old infected code
#it relates to an old version of the contact dict though so will not work anymore
#not deleting yet because it's Elise's code!
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

