

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()

from carport import models
import datetime
begin_time = datetime.datetime.strptime("08:11:11",'%H:%M:%S')
end_time = datetime.datetime.strptime("11:11:11",'%H:%M:%S')
# print(begin_time)
record_list1 = list(models.Record.objects.filter(begin_hours__gte=begin_time,begin_hours__lte=end_time))
print(record_list1[0])
#
# print(datetime.datetime.strptime("2019-06-16",'%Y-%m-%d')+datetime.timedelta(days = 1) == datetime.datetime.strptime("2019-06-17",'%Y-%m-%d'))

