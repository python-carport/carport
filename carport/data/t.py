import datetime
import time
a = datetime.datetime.strptime('13:15:20','%H:%M:%S')
b = datetime.datetime.strptime('21:02:36','%H:%M:%S')
print(b-a)