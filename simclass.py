import random
from collections import OrderedDict, defaultdict
from sets import Set

class Simulation(object):
  def __init__(self, movement, infection_chance):
    #self.movement = movement
    #Create a blank node for each position and initialise queue with initial positions
    self.locations = {x: Location(x) for x in movement}
    self.queue = defaultdict(list, {0: [People(v, x.iteritems(), infection_chance) for v,x in movement.items()]})
    #format of queue is {tick:[person,person,etc.]}
    self.stage = 0
    self.people = self.queue[0]
    self.moves_per_tick = {}
    self.infected_per_tick = {}
  def step(self):
    moves = []
    #empty queue for the step and move people
    for person in self.queue[self.stage]:
      try: 
        new_time, new_location = person.movement.next()
        self.queue[new_time].append(person)          
        moves.append((person.name, person.nextLocation))
        person.move(self.locations[person.nextLocation])
        person.nextLocation = new_location
      except StopIteration:
        # No more movement from that person
        print self.stage, str(person.name) + " end of cycle"


    
    #carry out infection on each locatio.add
    for cell in self.locations.itervalues():
      cell.infect()
    self.moves_per_tick[self.stage] = moves
    self.infected_per_tick[self.stage] = self.infected()
    self.stage+=1
    
  
  #utility functions
  def infected(self): return [person.name for person in self.queue[0] if person.infected]
  def positions(self):
    for name, location in self.locations.iteritems():
      inf = 'I' if  any(map(lambda x: x.infected, location.contents)) else ''
      print inf + ' ' + str(name) + ' - ' + ','.join(map(lambda x: str(x.name), location.contents))           
  def free(self):
    return [x for x in self.locations.values() if not x.contents]
      

#possible position 
class Location(object):
  def __init__(self, name):
    self.name     = name 
    self.contents = []
    self.infected = 0
  
  #trigger infection event on all present people
  def infect(self):
    if self.infected:
      for infected in range(0,self.infected):
        for x in self.contents: x.infect()
  
  #person entering location
  def into(self, p):
    self.contents.append(p)
    if p.infected: self.infected += 1
    
  #person leaving location
  def leave(self, p):
    self.contents.remove(p)
    if p.infected: self.infected -= 1

  def __str__():
    return 'Location ' + str(name)
  
#person class
class People(object):
  def __init__(self, name, move, infection_chance):
    self.name = name
    self.infectcount = 0
    self.infected = False
    self.infection_chance = infection_chance
    self.location = None
    time, location = move.next()
    self.nextLocation = location
    #iterator of movement locations and times       
    self.movement = move
  def infect(self):
    #infection logic
    if not self.infected:
      print self.name
      infection_chance = random.random()
      if infection_chance <= self.infection_chance:
          self.infected = True
          print str(self.name) + " has been infected"
        
    

  def move(self, new):
    if self.location: self.location.leave(self)
    self.infectcount = 0
    self.location = new
    new.into(self)

  def __str__():
    return 'Person ' + str(person.name)
