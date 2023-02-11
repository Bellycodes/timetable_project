from operator import truth
from time import time
from django.db import models
from django.contrib.auth.models import User
import math
import random 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date
# Create your models here.

time_slots = (
    ('8:00 - 10:00', '8:00 - 10:00'),
    ('10:00 - 12:00', '10:00 - 12:00'),
    ('12:00 - 02:00', '12:00 - 02:00'),
    ('02:00 - 04:00', '02:00 - 04:00'),
    ('04:00 - 06:00', '04:00 - 06:00'),
)

DAY_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05


class School(models.Model):
    name = models.CharField(max_length=200)
    
     
    def __str__(self):
        return self.name

class Course_lecturer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Coursecode(models.Model):
    name = models.CharField(max_length=200)
    number_of_students = models.CharField(max_length=65, null=True)
    courselecturers = models.ManyToManyField(Course_lecturer)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    coursecodes = models.ForeignKey(Coursecode, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    @property
    def get_coursecodes(self):
        return self.coursecodes

    def __str__(self):
        return self.name

class Lectureroom(models.Model):
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=0)


    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Time(models.Model):
    lecture_time = models.CharField(max_length=50, choices=time_slots, default=time_slots[0])

    def __str__(self):
        return self.lecture_time

class Course(models.Model):
    coursecode = models.ForeignKey(Coursecode, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    lecturer =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    courselecturer = models.ForeignKey(Course_lecturer, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    lectureroom = models.ForeignKey(Lectureroom, on_delete=models.CASCADE, null=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, blank= True, null=True)
    day = models.CharField(max_length=15, choices=DAY_OF_WEEK, null=True)
    number_of_classes_in_week = models.IntegerField(default=0)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']


    def set_lectureroom(self, lectureroom):
        course = Course.objects.get( self.course.id)
        course.lectureroom = lectureroom
        course.save()

    def set_time(self, time):
        course = Course.objects.get(pk = self.course.id)
        course.time = time
        course.save()


    def set_courselecturer(self, courselecturer):
        course = Course.objects.get(self.course.id)
        course.courselecturer = courselecturer
        course.save()

    def __str__(self):
        return str (self.coursecode)

    
    

