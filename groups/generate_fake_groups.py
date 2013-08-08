def gen():
	num_students = 60
	num_teachers = num_students/10
	class_size = 20
	friendship_group_size = 10

	from groups import *
	import random


	#make students
	s=range(num_students)

	#make teachers
	t=range(num_students,(num_students+num_teachers))

	class_list = []
	friendship_group_list = []
	
	#make classes
	for c in range(0,num_students,class_size):
		g = Group(range(c,(class_size+c)))
		class_list.append(g)
	
	#make friends (daw)
	for f in range(0,num_students,friendship_group_size):
		g = Group(range(f,(friendship_group_size+c)))
		friendship_group_list.append(g)

	return class_list,friendship_group_list


	
	







