import datetime

print(datetime.datetime.strptime("2019-06-16 19:58:28",'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days = 1))