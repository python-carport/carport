import xlrd
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()

from carport import models

book = xlrd.open_workbook('车位信息.xls')
sheet = book.sheet_by_index (0)

rows = sheet.nrows
cols = sheet.ncols

models.User.objects.all().delete()

id = 0

for i in range (2, rows):
    name = sheet.cell (i,1).value
    phone = sheet.cell (i,2).value
    car_license = sheet.cell (i,3).value

    models.User.objects.create(
        id = id,
        name = name,
        phone = phone,
        password= '123',
        remain= 30.0,
        credit = 5.0,

    )

    print(str(id)+"  "+name)
    id = id+1