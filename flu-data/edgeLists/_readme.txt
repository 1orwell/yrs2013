The four folders correspond to four strategies of calculating interactions or contacts from a set of CPRs (recall that an interaction between two motes is defined as a continuous sequence of CPRs, and a contact is the sum of all interactions). There are two parameters that are of importance: minimumDuration and dropoff. The parameter minimumDuration defines the minimum duration (in CPRs) for an interaction or contact (depending on the strategy - see below) to be considered. The dropoff parameter allows you to assume that the dataset might be missing CPRs, and dropoff allows you to define the number of CPRs that should be considered as a maximum dropoff value. The examples below should make this clear.

Important: The data files of edge lists provided always use minimumDuration = 1, dropoff = 0. 

Having said this, let's now consider two motes, id1 and id2. Assume that in the data, we find they they had CPRs at the following time steps:

1 
3 
4 
5 
8 
9 
10 
12 
23 
24 
25 
26 
28 
103 
112 
113 
114 
266 
267 
268 
269 
270

i.e. a total of 22 CPRs.

Here's the what the four strategies return by default (minimumDuration = 1, dropoff = 0):

addThenChop:
1	2	22

chopThenAdd:
1	2	22

chopThenCount:
1	2	9

justChop:
1	2	1
1	2	3
1	2	3
1	2	1
1	2	4
1	2	1
1	2	1
1	2	3
1	2	5

addThenChop and chopThenAdd both return the total number of 22 CPRs. This is relevant because this is the length of the contact, i.e. the weight of the edge in the graph between nodes 1 and 2. chopThenCount returns the number of interactions (there are nine). justChop returns the nine interactions separately, indicating the length of each interaction.

If you are curious about the parameters minimumDuration and dropoff, read on.

minimumDuration: defines the minimum duration of an interaction or contact to be considered relevant for a particular strategy. With minimumDuration = 2, dropoff = 0, we would get the following results:

addThenChop:
1	2	22

chopThenAdd:
1	2	18

chopThenCount:
1	2	5

justChop:
1	2	3
1	2	3
1	2	4
1	2	3
1	2	5

The first strategy, addThenChop, first adds all interactions and then applies the minimumDuration, i.e. in this case the minimumDuration is with regard to the contact. chopThenAdd applies the minimumDuration to the interactions, and since there are four interactions of length 1, these are disregarded. Hence the total is only 18 (the same applies for the other two strategies). In summary, minimumDuration is generally applied to interactions, except for the addThenChop strategy.

dropoff: defines the minimum CPR gap to be filled.

Consider the case minimumDuration = 1, dropoff = 1:

addThenChop:
1	2	25

chopThenAdd:
1	2	25

chopThenCount:
1	2	6

justChop:
1	2	5
1	2	5
1	2	6
1	2	1
1	2	3
1	2	5

What happens here is that gaps of 1 CPR (because dropoff = 1) are filled in. For example, even though that data say that there was a CPR at time steps 1, 3, 4, 5 etc. we now assume that there was also an interaction at time step 2 (because there is a gap of only one CPR between time step 1 and 3. The same applies for time steps 10, 12, and 26, 28. After this merging process, we are left with 6 interactions.