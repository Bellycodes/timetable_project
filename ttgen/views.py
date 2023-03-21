import random
from django.shortcuts import render, redirect
from . forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from .render import Render
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

class Data:
    def __init__(self):
        self._rooms = LectureRoom.objects.all()
        self._timeslots = TimeSlot.objects.all()
        self._lecturer = Lecturer.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()
        self._sections = Section.objects.all()

    def get_rooms(self): return self._rooms

    def get_lecturers(self): return self._lecturer

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_lecture_times(self): return self._timeslots
    
    def get_sections(self): return self._sections
    
    
data = Data()
    
class Schedule:
    def __init__(self, data):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): 
        return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = self._data.get_sections()
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            if n <= len(self._data.get_lecture_times()):
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_lecturer = course.lecturer.all()
                        newClass = Class(self._classNumb, dept, section, course)
                        self._classNumb += 1
                        newClass.set_lecture_time(self._data.get_lecture_times()[random.randrange(0, len(self._data.get_lecture_times()))])
                        newClass.set_room(self._data.get_rooms()[random.randrange(0, len(self._data.get_rooms()))])
                        newClass.set_lecturer(crs_lecturer[random.randrange(0, len(crs_lecturer))])
                        self._classes.append(newClass)
            else:
                n = len(self._data.get_lecture_times())
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_lecturer = course.lecturer.all()
                        newClass = Class(self._classNumb, dept, section, course)
                        self._classNumb += 1
                        newClass.set_lecture_time(self._data.get_lecture_times()[random.randrange(0, len(self._data.get_lecture_times()))])
                        newClass.set_room(self._data.get_rooms()[random.randrange(0, len(self._data.get_rooms()))])
                        newClass.set_lecturer(crs_lecturer[random.randrange(0, len(crs_lecturer))])
                        self._classes.append(newClass)

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(i+1, len(classes)):
                if (classes[i].lecture_time == classes[j].lecture_time) and \
                        (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
                    if classes[i].room == classes[j].room:
                        self._numberOfConflicts += 1
                    if classes[i].lecturer == classes[j].lecturer:
                        self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)



class Population:
    def __init__(self, size, data):
        self._size = size
        self._data = data
        self._schedules = [Schedule(self._data).initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules



class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0, data)
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
        crossoverSchedule = Schedule(data).initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule(data).initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0, data)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id
        self.department = dept
        self.course = course
        self.lecturer = None
        self.lecture_time = None
        self.room = None
        self.section = section

    def get_id(self): return self.section_id

    def get_dept(self): return self.department

    def get_course(self): return self.course

    def get_lecturer(self): return self.lecturer

    def get_lecture_time(self): return self.lecture_time

    def get_room(self): return self.room

    def set_lecturer(self, lecturer): self.lecturer = lecturer

    def set_lecture_time(self, lecture_time): self.lecture_time = lecture_time

    def set_room(self, room): self.room = room


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    for i in range(len(classes)):
        cls = {}
        cls["section"] = classes[i].section_id
        cls['dept'] = classes[i].department.dept_name
        cls['course'] = f'{classes[i].course.title} ({classes[i].course.code}, {classes[i].course.max_numb_students})'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['lecturer'] = f'{classes[i].lecturer.name} ({classes[i].lecturer.id})'
        cls['lecture_time'] = [classes[i].lecture_time.id, classes[i].lecture_time.day, classes[i].lecture_time.time]
        context.append(cls)
    return context

@login_required
def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE, data)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        print('\n\n\n\nIn while loop')
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        
        best_schedule = population.get_schedules()[0]
        schedule_classes = best_schedule.get_classes()
        print('Best schedule fitness:', best_schedule.get_fitness())
        print('Number of classes in schedule:', len(schedule_classes))
        if not schedule_classes:
            print('Empty schedule!')
        else:
            schedule = schedule_classes
            
            schedule.append(population.get_schedules()[0].get_classes())

    return render(request, 'ttgen/gentimetable.html', {'schedule': schedule, 'sections': Section.objects.all(),
                                              'times': TimeSlot.objects.all()})


#################################################################################
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'ttgen/dashboard.html'
    paginate_by = 4
    permission_classes = [IsAuthenticated]

    # Add your context variables here
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List of lecturers
        context['lecturers'] = Lecturer.objects.all()
        # List of courses
        context['courses'] = Course.objects.all()
        # List of Level
        context['level'] = Level.objects.all()
        # List of departments
        context['departments'] = Department.objects.all()
        # List of lecture room
        context['rooms'] = LectureRoom.objects.all()
        # List of lecture time
        context['times'] = TimeSlot.objects.all()
        # List of Section
        context['sections'] = Section.objects.all()

        return context


######################################################################################
# COURSE FUNCTIONS

@login_required
def add_courses(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.title} added sucessfully')
            obj.save()
            return redirect('ttgen:add-courses')

    context = {
        'form': form
    }
    return render(request, 'ttgen/add_courses.html', context)

@login_required
def edit_course(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.title} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'course': course,
        'form': form
    }
    return render(request, 'ttgen/edit_course.html', context)

@login_required
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        messages.error(request, f'Course deleted')
        return redirect('ttgen:dashboard')
    context = {
        'crs': crs,
    }
    return render(request, 'ttgen/delete_course.html', context)
 


######################################################################################
# LEVEL FUNCTIONS

@login_required
def add_level(request):
    form = LevelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.level} added sucessfully')
            obj.save()
            return redirect('ttgen:add-level')

    context = {
        'form': form
    }
    return render(request, 'ttgen/add_level.html', context)

@login_required
def edit_level(request, pk):
    level = Level.objects.get(id=pk)
    form = LevelForm(instance=level)
    
    if request.method == 'POST':
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.level} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'level': level,
        'form': form
    }
    return render(request, 'ttgen/edit_level.html', context)

@login_required
def delete_level(request, pk):
    level = Level.objects.filter(pk=pk)
    if request.method == 'POST':
        level.delete()
        messages.error(request, f'Level deleted')
        return redirect('ttgen:dashboard')
    context = {
        'level': level,
    }
    return render(request, 'ttgen/delete_level.html', context)

#################################################################################
# LECTURER FUNCTIONS
@login_required
def add_lecturer(request):
    form = LecturerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.name} added sucessfully')
            obj.save()
            return redirect('ttgen:add-lecturer')

    context = {
        'form': form
    }
    return render(request, 'ttgen/add_lecturer.html', context)

@login_required
def edit_lecturer(request, pk):
    lecturer = Lecturer.objects.get(id=pk)
    form = LecturerForm(instance=lecturer)
    
    if request.method == 'POST':
        form = LecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.name} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'lecturer': lecturer,
        'form': form
    }
    return render(request, 'ttgen/edit_lecturer.html', context)

@login_required
def delete_lecturer(request, pk):
    lecturer = Lecturer.objects.filter(pk=pk)
    if request.method == 'POST':
        lecturer.delete()
        messages.error(request, f'Lecturer deleted')
        return redirect('ttgen:dashboard')
    context = {
        'lecturer': lecturer,
    }
    return render(request, 'ttgen/delete_lecturer.html', context)
#################################################################################
# LECTURE ROOM FUNCITONS

@login_required
def add_lecture_room(request):
    form = LectureRoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.r_number} added sucessfully')
            obj.save()
            return redirect('ttgen:add-lectrooms')

    context = {
        'form': form
    }
    return render(request, 'ttgen/add_lectRooms.html', context)

@login_required
def edit_lecture_room(request, pk):
    room = LectureRoom.objects.get(id=pk)
    form = LectureRoomForm(instance=room)
    
    if request.method == 'POST':
        form = LectureRoomForm(request.POST, instance=room)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.r_number} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'room': room,
        'form': form
    }
    return render(request, 'ttgen/edit_lectRoom.html', context)

@login_required
def delete_lecture_room(request, pk):
    room = LectureRoom.objects.filter(pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.error(request, f'Lecture Room deleted')
        return redirect('ttgen:dashboard')
    context = {
        'room': room,
    }
    return render(request, 'ttgen/delete_room.html', context)

#################################################################################
# LECTURE TIME FUNCTIONS

@login_required
def add_lecture_time(request):
    form = TimeSlotForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.time} added sucessfully')
            obj.save()
            return redirect('ttgen:add-lecttime')

    context = {
        'form': form
    }
    return render(request, 'ttgen/add_time.html', context)

@login_required
def edit_lecture_time(request, pk):
    time = TimeSlot.objects.get(id=pk)
    form = TimeSlotForm(instance=time)
    
    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=time)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.time} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)

    context = {
        'time': time,
        'form': form
    }
    return render(request, 'ttgen/edit_lectTime.html', context)

@login_required
def delete_lecture_time(request, pk):
    time = TimeSlot.objects.filter(pk=pk)
    if request.method == 'POST':
        time.delete()
        messages.error(request, f'Lecture Time deleted')
        return redirect('ttgen:dashboard')
    context = {
        'time': time,
    }
    return render(request, 'ttgen/delete_time.html', context)

#################################################################################
# DEPARTMENTS FUNCTION

@login_required
def add_departments(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.dept_name} added sucessfully')
            obj.save()
            return redirect('ttgen:add-dept')
    context = {
        'form': form
    }
    return render(request, 'ttgen/add_depts.html', context)

@login_required
def edit_department(request, pk):
    department = Department.objects.get(id=pk)
    form = DepartmentForm(instance=department)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'{obj.dept_name} updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'department': department,
        'form': form
    }
    return render(request, 'ttgen/edit_deparment.html', context)

@login_required
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.error(request, f'Department deleted')
        return redirect('ttgen:dashboard')
    context = {
        'dept': dept,
    }
    return render(request, 'ttgen/delete_department.html', context)
#################################################################################
# SECTION FUNCTIONS

@login_required
def add_sections(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'Section added sucessfully')
            obj.save()
            return redirect('ttgen:add-sections')
    context = {
        'form': form
    }
    return render(request, 'ttgen/add_sections.html', context)

@login_required
def edit_section(request, pk):
    section = Section.objects.get(id=pk)
    form = SectionForm(instance=section)
    
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            obj = form.save()
            messages.info(request, f'Section updated sucessfully')
            obj.save()
            return redirect('ttgen:dashboard', pk=obj.pk)
            
    context = {
        'section': section,
        'form': form
    }
    return render(request, 'ttgen/edit_section.html', context)

@login_required
def delete_section(request, pk):
    section = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        section.delete()
        messages.error(request, f'Section deleted')
        return redirect('ttgen:dashboard')
    context = {
        'section': section,
    }
    return render(request, 'ttgen/delete.html', context)

#################################################################################

@login_required
def generate(request):
    return render(request, 'ttgen/generate_timetable.html', {})

#################################################################################

class Pdf(View):
    def get(self, request):
        params = {
            'request': request
        }
        return Render.render('ttgen/gentimetable.html', params)


