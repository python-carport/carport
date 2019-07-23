import datetime

print(datetime.datetime.strptime("2019-06-16",'%Y-%m-%d')+datetime.timedelta(days = 1) == datetime.datetime.strptime("2019-06-17",'%Y-%m-%d'))