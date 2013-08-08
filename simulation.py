'''Virus spreading simulation using movement of people as given by fake.py

Format is 
{id: {time : position}}

'''
#Options
fin = './days/50-0.dat'
chance_of_infection = 1/36.0


###
from sets import Set
import pickle, random
from collections import defaultdict
import time

data = pickle.load(open(fin))
coords = data['coords']
ms = data['movement']
class Simulation(object):
	def __init__(self, movement):
		#self.movement = movement
		#Create a blank node for each position and initialise queue with initial positions
		self.locations = {x: Location(x) for x in movement}
		self.queue = defaultdict(list, {0: [People(v, x.iteritems()) for v,x in movement.items()]})
		#format of queue is {tick:[person,person,etc.]}
		self.stage = 0
		self.people = self.queue[0]
	def step(self):
		#empty queue for the step and move people
		
		
		for person in self.queue[self.stage]:
			try:
				new_time, new_location = person.movement.next()
				self.queue[new_time].append(person)
				person.move(self.locations[person.nextLocation])
				person.nextLocation = new_location
			except StopIteration:
				# No more movement from that person
				print tick, str(person.name) + " end of cycle"


		
		#carry out infection on each locatio.add
		for cell in self.locations.itervalues():
			cell.infect()
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
	def __init__(self, name, move):
		self.name = name
		self.infectcount = 0
		self.infected = False
		self.location = None
		time, location = move.next()
		self.nextLocation = location
		#iterator of movement locations and times       
		self.movement = move
	def infect(self):
		#infection logic
		#if self.infectcount == 10: self.infected = True
		#elif self.infectcount > 5 and random.random() > 0.5: self.infected = True
		#self.infectcount += 1
		if self.infected == False:
			print self.name
			infection_chance = random.random()
			if infection_chance <= chance_of_infection:
					self.infected = True
					print str(self.name) + " has been infected"
				
		

	def move(self, new):
		if self.location: self.location.leave(self)
		self.infectcount = 0
		self.location = new
		new.into(self)
		moves.append((self.name, new.name))

	def __str__():
		return 'Person ' + str(person.name)



s = Simulation(ms)

s.people[32].infected = True
s.people[33].infected = True
s.people[34].infected = True
s.people[35].infected = True
#format: key = tick, value = list of infected people
infected_per_tick = dict()
moves_per_tick = {}
for tick in range(0, 2000):
	moves = []
	s.step()
	moves_per_tick[tick] = moves
	infected_per_tick[tick] = s.infected()

print 'Simulation finished'
print 'Writing to virus.dat file'
output = 'virus.dat'
out = {'coords': coords, 'virus': infected_per_tick, 'moves': moves_per_tick}
pickle.dump(out, open(output, 'w'))
print 'finished writing'




'''
print 'starting simulation'
s = Simulation(ms)
s.queue[0][0].infected = True



for tick in range(200,300):
	s.step()
	print 'step finished'
	print 'tick ' + str(tick)
	print '\n'
	#print s.infected()


print 'simulation finished'
'''
