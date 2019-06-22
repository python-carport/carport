from django.contrib import admin

from .models import User
from .models import Carport

admin.site.register(User)
admin.site.register(Carport)