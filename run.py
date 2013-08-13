import os
import fake
import simulation
import display
from groups.sim_group_move import generate_fake

option = raw_input('0. Real data \n1. Generated data\n')

if option == '0': 
  fake.process('generated.dat')
  simulation.simulate('generated.dat')
  display.display('generated-display.dat')
elif option == '1': 
  generate_fake(os.path.join(os.getcwd(), 'data','fake-virus.dat'))
  simulation.simulate('fake-virus.dat')
  display.display('fake-virus-display.dat')
else:
  print 'Invalid option'  


