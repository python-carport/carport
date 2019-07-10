import datetime
import json
import random
import time
# a = datetime.datetime.strptime('13:15:20','%H:%M:%S')
# b = datetime.datetime.strptime('21:02:36','%H:%M:%S')
# print(b-a)

c={}
# c = {'a':2}
c.update({'b':c.get('b',0)+1})
print(sorted(c.items(), key = lambda x: x[1], reverse = True)[0][0])
d = {(1,2,3), (2,2,3)}
print(random.randint(1,1))
print(tuple(c.keys())[0])

h = "[('22', '13905180721'), ('84', '13376065277'), ('31', '18652030707'), ('99', '18905149889'), ('88', '13905180721'), ('56', '13851774016'), ('77', '18922890829'), ('100', '13357836618'), ('6', '13512533542')]"
print(eval(h).__len__())
for i in eval(h):
	print(i)