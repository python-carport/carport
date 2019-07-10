import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()


from carport import models
models.User.objects.all().delete()
models.Carport.objects.all().delete()
models.Link.objects.all().delete()

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