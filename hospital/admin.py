from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(Appointment)
