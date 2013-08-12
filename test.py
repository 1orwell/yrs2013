import pickle
f = open('flu-data/movement.dat')
mv = pickle.load(f)
dic = {}

for i in range(len(mv.values())):
    for value in mv.values()[i]:
        mv.values()[i][value] = mv.values()[i][value]/2, (mv.values()[i][value]/2)+20

    dic[i] = mv.values()[i]

print dic



















#def set_of_times(mv):
 #   for i in mv.values():
  #      keylist.update(i.keys())
   # return keylist
    #return mv.values().keys()

#print keylist
#print len(mv[1])

