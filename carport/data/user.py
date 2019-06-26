import xlrd
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")# project_name 项目名称
django.setup()

from carport import models