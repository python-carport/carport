import datetime
import decimal
import random

import xlrd
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()


def trim(s):
    length = len(s)

    if length > 0:
        for i in range(length):
            if s[i] != ' ':
                break
        j = length - 1
        while s[j] == ' ' and j >= i:
            j -= 1
        s = s[i:j + 1]

    return s

def date_diff(begin_time, end_time):
	diff = end_time - begin_time
	diff_str = str(diff)
	if diff_str.find(' days, ') > 0:
		d = int(diff_str.split(' days, ')[0])
		h = diff.seconds/60/60
		return d*24+h
	elif diff_str.find(' day, ') > 0:
		h = diff.seconds / 60 / 60
		return 24 + h
	else:
		h = diff.seconds/60/60
		return h

from carport import models
# from django.db import models

book = xlrd.open_workbook('记录.xls')#打开一个excel
sheet = book.sheet_by_index(0)#根据顺序获取sheet

rows = sheet.nrows
cols = sheet.ncols

a=0

models.Record.objects.all().delete()
# 13
#6430 出入车辆号码不一  入：津JC30L0  出：苏AC30L0

for i in range(2, rows):
	id = sheet.cell(i, 0).value
	car_license = trim(sheet.cell(i, 1).value)
	type = trim(sheet.cell(i, 3).value)
	local = trim(sheet.cell(i, 5).value)
	account = trim(sheet.cell(i, 7).value)
	total_time = float(str(trim(sheet.cell(i, 8).value)).split('小时')[0]) + (
					float(str(trim(sheet.cell(i, 8).value)).split('小时')[1].split('分')[0]) / 60)
	begin_time = sheet.cell(i, 9).value
	end_time = sheet.cell(i, 12).value

	if type == '月租车':

		try:
			site = models.Link.objects.get(car_license = car_license).carport_site
		except:
			print(car_license)
			a += 1
			continue
	bt=datetime.datetime.strptime(str(begin_time).split(' ')[0],'%Y-%m-%d')
	et=datetime.datetime.strptime(str(end_time).split(' ')[0],'%Y-%m-%d')
	bh=datetime.datetime.strptime(str(begin_time).split(' ')[1],'%H:%M:%S')
	eh=datetime.datetime.strptime(str(end_time).split(' ')[1],'%H:%M:%S')

	if bt==et:
		models.Record.objects.create(
			car_license=car_license,
			type=type,
			local=local,
			account=account,
			total_time=total_time,
			begin_time=begin_time,
			end_time=end_time,
			carport_site=site,
			weekday= bt.weekday(),
			group= id,
			begin_hours=bh,
			end_hours=eh,
		)
	else:
		# 第一天
		first_day_time = date_diff(datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime(str(begin_time).split(' ')[0]+" 23:59:59",'%Y-%m-%d %H:%M:%S'))
		models.Record.objects.create(
			car_license = car_license ,
			type = type ,
			local = local ,
			account = account ,
			total_time = first_day_time,
			begin_time = begin_time ,
			end_time = datetime.datetime.strptime(str(begin_time).split(' ')[0]+" 23:59:59",'%Y-%m-%d %H:%M:%S') ,
			carport_site = site ,
			weekday = bt.weekday() ,
			group = id ,
			begin_hours=bh,
			end_hours=datetime.datetime.strptime("23:59:59",'%H:%M:%S'),
		)
		bt = bt + datetime.timedelta(days = 1)
		total_time = total_time - first_day_time
		# 中间天数
		while bt < et:
			models.Record.objects.create(
				car_license=car_license,
				type=type,
				local=local,
				account=account,
				total_time=24,
				begin_time=datetime.datetime.strptime(str(bt).split(' ')[0] + " 00:00:00" , '%Y-%m-%d %H:%M:%S'),
				end_time=datetime.datetime.strptime(str(bt).split(' ')[0]+" 23:59:59",'%Y-%m-%d %H:%M:%S'),
				carport_site=site,
				weekday=bt.weekday(),
				group=id,
				begin_hours=datetime.datetime.strptime("00:00:00",'%H:%M:%S'),
			    end_hours = datetime.datetime.strptime("23:59:59",'%H:%M:%S'),
			)
			bt=bt+datetime.timedelta(days = 1)
			total_time -= 24
		# 最后一天
		models.Record.objects.create(
			car_license = car_license ,
			type = type ,
			local = local ,
			account = account ,
			total_time = total_time ,
			begin_time = datetime.datetime.strptime(str(bt).split(' ')[0] + " 00:00:00" , '%Y-%m-%d %H:%M:%S'),
			end_time = end_time ,
			carport_site = site ,
			weekday = bt.weekday() ,
			group = id ,
			begin_hours=datetime.datetime.strptime("00:00:00",'%H:%M:%S'),
			end_hours=eh,
		)
	print(i)

