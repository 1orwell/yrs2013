from generate_fake_groups import *
from collections import OrderedDict
import random

#Options
num_students = 60


period_list, fg_list = gen(num_students)

'''
Order of day:
Period/class 1
Period/class 2
Break
Period/class 3
Lunch
Period/class 4
Period/class 5
Break
Period/class 6

Each period and lunch is 55m
Break is 10m
in between every break/period/lunch there is a 5m transition

Ticks are 20 seconds
Therefore
period/lunch = 165 ticks
break = 30 ticks
transition = 15 ticks
'''

#initialises dict with everyone in starting locations
movement_dict = dict()
for person in range(num_students):
	movement_dict[person] = OrderedDict({0 : person})


#gives each class random locaton
for class_list in period_list:
	for c in class_list:
		loc = random.randint(0,num_students-1)
		c.location = loc

#gives each friendship group a random location to take place in
for fg in fg_list:
	loc = random.randint((num_students/2),(num_students-1))
	fg.location = loc

#day sequence
sequence = ['class','class','break','class','lunch','class','class','break','class']

#dict of times for period type
wait_dict = {'class':55,'break':10,'lunch':55}


#moves people (surprise, surprise)
def move(person,new,current,time,event):
	trans_time = 5
	trans_tick = 3 * trans_time
	
	dist = person.location
	for tick in range(trans_tick):
		
		movement_dict[person] = 
	



#this moves everyone to classes at start of day
class_list = period_list[0]

time = 0 
wait = 0
for c in class_list:
	for person in c.members:
		move(person,c.location.wait)

#this moves people when event changes
period = 0



for event in sequence:
	time += wait_dict[event]
	wait = wait_dict[event]
	#if event is class, base movement off classes
	if event == 'class'
		class_list = period_list[period]
		for c in class_list:
			for person in c.members:
				current = 
				new = c.location
				move(person,new,current,wait,event)
	
	#if event is break/lunch, base movement off friendship groups
	if event == 'break' or event == 'lunch':
		for fg in fg_list:
			for person in fg.members:
				current = movement_dict[person][
				new = fg.location
				move(person,new,current,time,event)
	
	#if event is class, increment period so it knows which period and hence which classes to look at next class type
	if event == 'class': period += 1	




