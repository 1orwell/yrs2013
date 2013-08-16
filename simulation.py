
from sets import Set
import pickle, random, os
from collections import defaultdict
import simclass
'''Virus spreading simulation using movement of people as given by fake.py

input format is 
{id: {time : position}}

'''
#Options
#fin = './days/790-0.dat'
#fin = './groups/fake_groups.dat' 
chance_of_infection = 1/36.0

default = './days/100-0.dat'

###
def simulate(fin):
  fin = os.path.join('data',fin)
  data = pickle.load(open(fin))
  coords = data['coords']
  ms = data['movement']
  
  s = simclass.Simulation(ms, chance_of_infection)
  #set infected people
  s.people[32].infected = True
  s.people[33].infected = True
  s.people[34].infected = True
  s.people[35].infected = True
  #format: key = tick, value = list of infected people
  for tick in range(0, 2000):
    s.step()

  print 'Simulation finished'
  print 'Writing to file'
  fileName, fileExtension = os.path.splitext(fin) 
  output = fileName+'-display'+fileExtension
  out = {'coords': coords, 'virus': s.infected_per_tick, 'moves': s.moves_per_tick}
  pickle.dump(out, open(output, 'wb'))
  print 'finished writing'

if __name__ == '__main__':
  simulate(default)


