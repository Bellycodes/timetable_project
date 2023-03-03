from django.forms import ModelForm
from. models import *
from django import forms

class LectureRoomForm(ModelForm):
    class Meta:
        model = LectureRoom
        labels = {
            "r_number": "Room ID",
            "seating_capacity": "Capacity"
        }
        fields = [
            'r_number',
            'seating_capacity'
        ]


class LecturerForm(ModelForm):
    class Meta:
        model = Lecturer
        labels = {
            "uid": "Teacher UID",
            "name": "Full Name"
        }
        fields = [
            'uid',
            'name',
        ]


class TimeSlotForm(ModelForm):
    class Meta:
        model = TimeSlot
        fields = [
            'pid',
            'time',
            'day'
        ]
        widgets = {
            'pid': forms.TextInput(),
            'time': forms.Select(),
            'day': forms.Select(),
        }
        labels = {
            "pid": "Meeting ID",
            "time": "Time",
            "day": "Day of the Week"
        }


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'lecturer']
        labels = {
            "code": "Course Code",
            "title": "Course Title",
            # "max_numb_students": "Course Capacity",
            "lecturer": "Course Lecturer"
        }


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'level', 'courses']
        labels = {
            "dept_name": "Department Name",
            "courses": "Corresponding Courses",
            'level': "Level"
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'department', 'num_class_in_week']
        labels = {
            "section_id": "Section ID",
            "department": "Corresponding Department",
            "num_class_in_week": "Classes Per Week"
        }
