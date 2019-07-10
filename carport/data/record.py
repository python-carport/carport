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
	total_time = trim(sheet.cell(i, 8).value)
	begin_time = sheet.cell(i, 9).value
	end_time = sheet.cell(i, 12).value

	if type == '月租车':
		a+=1
		try:
			site = models.Link.objects.get(car_license = car_license)
		except:
			print(car_license)

	models.Record.objects.create(
		id = id,
		car_license = car_license,
		type = type,
		local = local,
		account = account,
		total_time = decimal.Decimal(str(total_time).split('小时')[0])+(decimal.Decimal(str(total_time).split('小时')[1].split('分')[0])/60),
		begin_time = begin_time,
		end_time = end_time,
		carport_site = str(random.randint(1, 130)),
	)
	# print(id)
print(a)