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

movement_dict = dict()
for person in range(num_students):
	movement_dict[person] = OrderedDict({0 : person})


for class_list in period_list:
	for c in class_list:
		loc = random.randint(0,num_students-1)
		c.location = loc

loc = 10
for fg in fg_list:
	loc = random.randint((num_students/2),(num_students-1))
	fg.location = loc

def move(person,location,wait):
	trans_time = 5
	trans_tick = 3 * trans_time


sequence = ['class','class','break','class','lunch','class','class','break','class']

wait_dict = {'class':55,'break':10,'lunch':55}


class_list = period_list[0]
wait = 0
for c in class_list:
	for person in c.members:
		move(person,c.location.wait)

period = 0
for event in sequence:
	class_list = period_list[period]
	wait = wait_dict[event]
	for c in class_list:
		for person in c.members:
			move(person,c.location,wait)

	if event == 'class': period += 1	




