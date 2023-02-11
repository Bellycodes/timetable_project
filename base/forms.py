from time import time
from django import forms
from django.forms import ModelForm
from .models import *
from django import forms

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['lecturer']

        widgets = {
            'time': forms.Select(),
            'day': forms.Select()
        }

        labels = {
            'time': 'Time',
            'day': 'Day of the week'
        }
    
    
