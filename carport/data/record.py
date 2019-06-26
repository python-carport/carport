import xlrd
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()

from carport import models
# from django.db import models

book = xlrd.open_workbook('记录.xls')#打开一个excel
sheet = book.sheet_by_index(0)#根据顺序获取sheet

rows = sheet.nrows
cols = sheet.ncols

models.Record.objects.all().delete()
j=0
# 13
#6430 出入车辆号码不一  入：津JC30L0  出：苏AC30L0
for i in range(2, rows):
	id = sheet.cell(i, 0).value
	car_license = sheet.cell(i, 1).value
	type = sheet.cell(i, 3).value
	local = sheet.cell(i, 5).value
	account = sheet.cell(i, 7).value
	total_time = sheet.cell(i, 8).value
	begin_time = sheet.cell(i, 9).value
	end_time = sheet.cell(i, 12).value

	models.Record.objects.create(
		id = id,
		car_license = car_license,
		type = type,
		local = local,
		account = account,
		total_time = total_time,
		begin_time = begin_time,
		end_time = end_time,
	)
	print(id)
