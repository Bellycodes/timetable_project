from multiprocessing import context
from django.http import request, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View



# Create your views here.

#courses = [
   # {'id': 1, 'Course': 'CPE501'},
    #{'id': 2, 'course': 'CPE503'},
    #{'id': 3, 'course': 'CPE505'},
   # {'id': 4, 'course': 'CPE507'},
#]

def loginUser(request):
    loginpage = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This user is not registered')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or Password')


    context = { 'loginpage': loginpage}
    return render(request, 'base/loginpage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def signUp(request):
    signupform = UserCreationForm()

    if request.method == 'POST':
        
        signupform = UserCreationForm(request.POST)
        if signupform.is_valid():
            user = signupform.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'An error occured')

    return render(request, 'base/loginpage.html', {'signupform': signupform})


def home(request):
    d = request.GET.get('d') if request.GET.get('d') != None else ''
    courses = Course.objects.filter(department__name__icontains = d) 
    courses = Course.objects.filter(level__name__icontains = d) 
    courses = Course.objects.filter (coursecode__name__icontains = d)
    

    departments = Department.objects.all()
    course_count = courses.count()
    context = {'courses': courses, 'departments': departments, 'course_count': course_count}
    return render(request, 'base/homepage.html', context)


def course(request, pk):
    course = Course.objects.get(id=pk)
    context = {'course': course}
    return render(request, 'base/course.html', context)


@login_required(login_url='login')
def addCourse(request):
    form = CourseForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            course = form.save(commit=False)
            course.lecturer = request.user
            course.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/course-form.html', context)



def editCourse(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)


    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/course-form.html', context)

def deleteCourse(request, pk):
    course = Course.objects.get(id=pk)


    if request.method == 'POST':
        course.delete()
        return redirect('home')
    return render(request, 'base/deleteform.html', {'object':course})


#####################################################
# views.py

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

class data:
    def __init__(self):
        self.lectureroom = Lectureroom.objects.all()
        self.time = Time.objects.all()
        self.courselecturer = Course_lecturer.objects.all()
        self.coursecode = Coursecode.objects.all()
        self.depts = Department.objects.all()
        self.course = Course.objects.all()

    def get_lecturerooms(self): return self.lectureroom

    def get_courselecturers(self): return self.courselecturer

    def get_coursecodes(self): return self.coursecode

    def get_depts(self): return self.depts

    def get_times(self): return self.time

class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True


    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes


    def get_numbOfConflicts(self): return self._numberOfConflicts


    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness


    def initialize(self):
        courses = Course.objects.all()
        for course in courses:
            dept = course.department
            n = course.number_of_classes_in_week 
            if n <= len(Time.objects.all()):
                coursecodes = Coursecode.objects.all()
                for coursecode in coursecodes:
                    for i in range(n // len(coursecodes)):
                        crs_inst = Course_lecturer.objects.all()
                        newClass = Class(self._classNumb, dept, course.id, coursecode)
                        self._classNumb += 1
                        newClass.set_Time(data.get_Times()[random.randrange(0, len(Time.objects.all()))])
                        newClass.set_lectureroom(data.get_lecturerooms()[random.randrange(0, len(data.get_lecturerooms()))])
                        newClass.set_courselecturer(crs_inst[random.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
            else:
                n = len(Time.objects.all())
                coursecodes = dept.coursecodes.all()
                for coursecode in coursecodes:
                    for i in range(n // len(coursecodes)):
                        crs_inst = coursecode.courselecturer.all()
                        newClass = Class(self._classNumb, dept, course.id, coursecode)
                        self._classNumb += 1
                        newClass.set_Time(data.get_Times()[random.randrange(0, len(Time.objects.all()))])
                        newClass.set_lectureroom(data.get_lecturerooms()[random.randrange(0, len(data.get_lecturerooms()))])
                        newClass.set_courselecturer(crs_inst[random.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)

        return self


    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].lectureroom.capacity < int(classes[i].coursecode.number_of_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].time == classes[j].time) and \
                            (classes[i].course.id != classes[j].course.id) and (classes[i].course == classes[j].course):
                        if classes[i].lectureroom == classes[j].lectureroom:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].courselecturer:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)

class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if random.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > random.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[random.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop

class Class:
    def __init__(self, id, dept, Course, coursecode):
        self.Course.id = id
        self.department = dept
        self.coursecode = coursecode
        self.courselecturer = None
        self.time = None
        self.lectureroom = None
        self.course = Course 

    def get_id(self): return self.course.id

    def get_dept(self): return self.department

    def get_coursecode(self): return self.coursecode

    def get_courselecturer(self): return self.courselecturer

    def get_Time(self): return self.time

    def get_lectureroom(self): return self.lectureroom

    def set_courselecturer(self, courselecturer): self.courselecturer = courselecturer

    def set_time(self, time): self.time = time

    def set_lectureroom(self, lectureroom): self.lectureroom = lectureroom


data = data()


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["course"] = classes[i].course.id
        cls['dept'] = classes[i].department.name
        cls['coursecode'] = f'{classes[i].coursecode.name} ({classes[i].coursecode.name}, ' \
                        f'{classes[i].coursecode.number_of_students}'
        cls['lectureroom'] = f'{classes[i].lectureroom.name} ({classes[i].lectureroom.capacity})'
        cls['courselecturer'] = f'{classes[i].courselecturer.name} ({classes[i].courselecturer.name})'
        cls['time'] = [classes[i].time.lecture_time, classes[i].course.day]
        context.append(cls)
    return context

def timetable(request): 
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    return render(request, 'base/timetable.html', {'schedule': schedule, 'courses': Course.objects.all(),
                                              'times': Time.objects.all()})

############################################################################

class Pdf(View):
    def get(self, request):
        params = {
            'request': request
        }
        return render.render('base/generate.html', params)







