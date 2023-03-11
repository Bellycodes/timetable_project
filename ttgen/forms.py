from. models import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class LectureRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('r_number', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('seating_capacity', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        )
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


class LecturerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('uid', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        )
    class Meta:
        model = Lecturer
        labels = {
            "uid": "Lecturer UID",
            "name": "Full Name"
        }
        fields = [
            'uid',
            'name',
        ]


class TimeSlotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('pid', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('time', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('day', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        )
    class Meta:
        model = TimeSlot
        fields = [
            'pid',
            'time',
            'day'
        ]
        labels = {
            "pid": "Time ID",
            "time": "Time",
            "day": "Day of the Week"
        }


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('code', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('max_numb_students', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('lecturer', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        )  
    class Meta:
        model = Course
        fields = ['code', 'title', 'max_numb_students', 'lecturer']
        labels = {
            "code": "Course Code",
            "title": "Course Title",
            "max_numb_students": "Course Capacity",
            "lecturer": "Course Lecturer"
        }


class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('dept_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('level', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('courses', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        ) 
    class Meta:
        model = Department
        fields = ['dept_name', 'level', 'courses']
        labels = {
            "dept_name": "Department Name",
            "courses": "Corresponding Courses",
            'level': "Level"
        }


class SectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('section_id', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('num_class_in_week', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Add')
        ) 
    class Meta:
        model = Section
        fields = ['section_id', 'department', 'num_class_in_week']
        labels = {
            "section_id": "Section ID",
            "department": "Corresponding Department",
            "num_class_in_week": "Classes Per Week"
        }
