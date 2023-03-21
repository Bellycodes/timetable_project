from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ttgen'

urlpatterns = [

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('add-lecturers/', views.add_lecturer, name='add-lecturer'),
    path('edit-lecturer/<pk>/', views.edit_lecturer , name='edit-lecturer'),
    path('delete-lecturer/<pk>/', views.delete_lecturer, name='delete-lecturer'),

    path('add-lecture-rooms/', views.add_lecture_room, name='add-lectrooms'),
    path('edit-lecture_room/<pk>/', views.edit_lecture_room, name='edit-lectroom'),
    path('delete-lecture_room/<pk>/', views.delete_lecture_room, name='delete-lectroom'),

    path('add-lecture-times/', views.add_lecture_time, name='add-lecttime'),
    path('edit-lecture-time/<pk>/', views.edit_lecture_room, name='edit-lecttime'),
    path('delete-lecture-time/<pk>/', views.delete_lecture_time, name='delete-lecttime'),

    path('add-courses/', views.add_courses, name='add-courses'),
    path('edit-course/<pk>/', views.edit_course, name='edit-course'),
    path('delete-course/<pk>/', views.delete_course, name='delete-course'),
    
    path('add-levels/', views.add_level, name='add-level'),
    path('edit-level/<pk>/', views.edit_level, name='edit-level'),
    path('delete-level/<pk>/', views.delete_level, name='delete-level'),


    path('add-departments/', views.add_departments, name='add-dept'),
    path('edit-department/<pk>/', views.edit_department, name='edit-dept'),
    path('delete-department/<pk>/', views.delete_department, name='delete-dept'),

    path('add-sections/', views.add_sections, name='add-sections'),
    path('edit-section/<pk>/', views.edit_section, name='edit-section'),
    path('delete-section/<pk>/', views.delete_section, name='delete-section'),

    path('generate_timetable/', views.generate, name='generate'),

    path('timetable_generation/', views.timetable, name='timetable'),
    path('timetable_generation/render/pdf', views.Pdf.as_view(), name='pdf'),

]
