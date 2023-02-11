import json
from unicodedata import name
from django import forms
from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Course)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Lectureroom)
admin.site.register(Level)
admin.site.register(Semester)
admin.site.register(Coursecode)
admin.site.register(Course_lecturer)
admin.site.register(Time)





