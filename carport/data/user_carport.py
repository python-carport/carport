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

book = xlrd.open_workbook('车位信息.xls')
sheet = book.sheet_by_index (0)

rows = sheet.nrows
cols = sheet.ncols

models.User.objects.all().delete()
models.Carport.objects.all().delete()
models.Link.objects.all().delete()

id = 0
for i in range (1, rows):
    name = trim(sheet.cell (i,1).value)
    phone = trim(str(sheet.cell (i,2).value).split(".")[0])
    car_license = trim(sheet.cell (i,3).value)
    carport_site = trim(str(sheet.cell (i,4).value).split(".")[0])
    try:
        models.User.objects.get(phone = phone)
    except:
        models.User.objects.create(
            name = name,
            phone = phone,
            password= '123',
            remain= 30.0,
            credit = 5.0,
        )

    try:
        models.Carport.objects.get(site = carport_site)
    except:
        models.Carport.objects.create(
            site = carport_site,
            current_car_license = '',
            owner_phone = phone
        )

    models.Link.objects.create(
        id = id,
        car_license = car_license,
        carport_site = carport_site,
        owner_phone = phone
    )


    print(str(id)+"  "+name)
    id = id+1

models.User.objects.create(
            name = 'x',
            phone = '1',
            password= '1',
            remain= 30.0,
            credit = 5.0,
        )
models.User.objects.create(
            name = 'x',
            phone = '2',
            password= '2',
            remain= 30.0,
            credit = 5.0,
        )