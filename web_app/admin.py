from django.contrib import admin
from .models import Person, ElectroCar, User
# Register your models here.

admin.site.register(Person)
admin.site.register(ElectroCar)
admin.site.register(User)