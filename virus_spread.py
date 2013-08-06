#This module is designed to simulate the virus spread throughout the school

from node_interactions import get_dict_of_all_contacts, calculateMaxTime








def simple_virus():
    infected = [1]
    
    dict_of_all_contacts = get_dict_of_all_contacts('fake-data/moteFiles')
    maxtime = calculateMaxTime(dict_of_all_contacts)

    print dict_of_all_contacts
    
    for tick in range(0,maxtime+1):
        print "Tick",tick

        for infected_node in infected:
            time_dict = dict_of_all_contacts[infected_node]
            if tick in time_dict:
                interactions = time_dict[tick]
                infected.append(time_dict[tick])
            else:
                interactions="nothing"
            if interactions != "nothing":
                #print "Node",node,"interacts with",interactions
                continue

    return infected

infected = simple_virus()
print infected

