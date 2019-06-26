from django.contrib import admin

from .models import User , Order , Record
from .models import Carport

admin.site.register(User)
admin.site.register(Carport)
admin.site.register(Order)
admin.site.register(Record)