from generate_fake_groups import *
from collections import OrderedDict
import random,pickle



#Options
num_students = 60
num_people = num_students + (num_students/10)

def generate_fake(fin):
  #gen function from generate_fake_groups
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

  #coords definition
  coords = []

  wrap = 11 #11 positons per row, ie range(0,11) will give you 11 positions
  col_length = num_people/wrap

  for x in range(wrap):
    for y in range(col_length):
      coords.append((x,y))

  #initialises dict with everyone in starting locations
  movement_dict = dict()
  for person in range(num_people):
    movement_dict[person] = OrderedDict({0 : person})


  #gives each class random locaton
  for class_list in period_list:
    for c in class_list:
      loc = random.randint(0,(num_students-1))
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
  def move(person,new,current,time):
    trans_time_mins = 5
    trans_tick = 3 * trans_time_mins
    
    if new != current:
      #work out where they are x and y from linear position
      current_integer_x = current % wrap
      current_integer_y = current // wrap

      #ditto for new locations
      new_integer_x = new % wrap
      new_integer_y = new // wrap

      #work out how far they need to travel in x & y
      x_dist = new_integer_x - current_integer_x
      y_dist = new_integer_y - current_integer_y

      #work out how far they need to move per tick
      x_dist_per_tick = float(x_dist) / float(trans_tick)
      y_dist_per_tick = float(y_dist) / float(trans_tick)

      
      x_moved = float(current_integer_x)
      y_moved = float(current_integer_y)
      for tick in range(trans_tick):
        x_moved += x_dist_per_tick
        y_moved += y_dist_per_tick
        linear_pos = int(x_moved) + wrap*int(y_moved)
        movement_dict[person][time+tick] = linear_pos
    else:
      movement_dict[person][time+14] = current
      #on last tick move person rest of distance
      #because it is further away than the intervals due to integer division
      
      


  #this moves everyone to classes at start of day
  class_list = period_list[0]

  time = 0 
  wait = 0
  for c in class_list:
    for person in c.members:
      current = person #name is first position
      new = c.location
      event = 'class'
      move(person,new,current,time)
    for person in c.teachers:
      current = person #name is first position
      new = c.location
      event = 'class'
      move(person,new,current,time)

  time += 15 #move time up as transitions have taken place

  #this moves people when event changes
  period = 0



  for event in sequence:
    time += wait_dict[event]
    wait = wait_dict[event]
    #if event is class, base movement off classes
    if event == 'class':
      class_list = period_list[period]
      for c in class_list:
        for person in c.members:
          
          current = movement_dict[person][time-wait-1] #current location
          new = c.location
          move(person,new,current,time)
        for teacher in c.teachers:
          #current = movement_dict[teacher][time-wait] #current location
          #new = c.location
          #move(teacher,new,current,time)
          pass
      #increment period so it knows which period and hence which classes to look at next class type
      period += 1
    
    #if event is break/lunch, base movement off friendship groups
    if event == 'break' or event == 'lunch':
      for fg in fg_list:
        for person in fg.members:
          current = movement_dict[person][time-wait-1] #current location
          new = fg.location
          move(person,new,current,time)
     
    
    time += 15 #transitions take place so time must increase



  out = {'coords': coords, 'movement': movement_dict}
  output = fin 
  pickle.dump(out, open(output, 'w'))

if __name__ == '__main__':
  generate_fake('fake_groups.dat')
  	











