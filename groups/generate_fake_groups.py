def gen(num_students):
	num_teachers = num_students/10
	class_size = 20
	friendship_group_size = 10

	from groups import *
	import random


	period_list = []
	friendship_group_list = []
	
	#make classes
	for p in range(6):
		class_list = []
		#make students
		s=range(num_students)
		#make teachers
		t=range(num_students,(num_students+num_teachers))

		for c in range(0,num_students,class_size):
			g = Group()
			for n in range(class_size):
				student = random.choice(s)
				s.remove(student)
				g.members.append(student)
			for n in range(2):
				teacher = random.choice(t)
				t.remove(teacher)
				g.teachers.append(teacher)
			class_list.append(g)

		period_list.append(class_list)
	#make friends (daw)

	s = range(num_students)

	for f in range(0,num_students,friendship_group_size):
		g = Group()
		for n in range(friendship_group_size):
			friend = random.choice(s)
			s.remove(friend)
			g.members.append(friend)

		friendship_group_list.append(g)

	return period_list,friendship_group_list


	
	







