#This module is designed to simulate the virus spread throughout the school

from node_interactions import get_dict_of_all_contacts, calculateMaxTime



#1 in 36 chance of being infected
from random import randint



def simple_virus():
    infected = [1]

    print 'calculating contacts... '
    dict_of_all_contacts = get_dict_of_all_contacts('fake-data/moteFiles')

    maxtime = calculateMaxTime(dict_of_all_contacts)

    #print dict_of_all_contacts

    #tick through time
    for tick in range(0,maxtime+1):
        print "Tick",tick

        new_infected = []
        
        #for every infected node...
        for infected_node in infected:
            #get the dictionary of its interactions
            time_dict = dict_of_all_contacts[infected_node]
            #check if it interacts in this time frame
            if tick in time_dict:
                #iterate through all interactions between infected and targets
                for interaction in time_dict[tick]:
                    #check they haven't been infected this tick or in an earlier tick
                    if interaction not in infected:
                        if interaction not in new_infected:
                            #do random stuff to see chance of being infected
                            infection_chance = randint(1,36)
                            if infection_chance == 36:
                                new_infected.append(interaction)

        infected.extend(new_infected)
        #print infected
        
    return infected

infected = simple_virus()
print infected

