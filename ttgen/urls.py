from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('help', views.help, name='help'),
    path('terms', views.terms, name='terms'),
    path('contact', views.contact, name='contact'),

    path('admin_dashboard', views.admindash, name='admindash'),

    path('add_lecturer', views.addLecturer, name='add_lecturer'),
    path('lecturers_list/', views.inst_list_view , name='edit_lecturer'),
    path('delete_lecturer/<int:pk>/', views.delete_lecturer, name='delete_lecturer'),

    path('add_rooms', views.addRooms, name='addRooms'),
    path('rooms_list/', views.room_list, name='editrooms'),
    path('delete_room/<int:pk>/', views.delete_lecture_room, name='delete_lecture_room'),

    path('add_timings', views.addTimings, name='addTimings'),
    path('timings_list/', views.lecture_time_list_view, name='edit_lecture_time'),
    path('delete_lecture_time/<str:pk>/', views.delete_lecture_time, name='delete_letcure_time'),

    path('add_courses', views.addCourses, name='addCourses'),
    path('courses_list/', views.course_list_view, name='editcourse'),
    path('delete_course/<str:pk>/', views.delete_course, name='deletecourse'),

    path('add_departments', views.addDepts, name='addDepts'),
    path('departments_list/', views.department_list, name='editdepartment'),
    path('delete_department/<int:pk>/', views.delete_department, name='deletedepartment'),

    path('add_sections', views.addSections, name='addSections'),
    path('sections_list/', views.section_list, name='editsection'),
    path('delete_section/<str:pk>/', views.delete_section, name='deletesection'),

    path('generate_timetable', views.generate, name='generate'),

    path('timetable_generation/', views.timetable, name='timetable'),
    path('timetable_generation/render/pdf', views.Pdf, name='pdf'),

]
