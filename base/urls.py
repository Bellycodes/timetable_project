from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout-user/', views.logoutUser, name="logout-user"),
    path('signup/', views.signUp, name="signup"),


    path('', views.home, name="home"),
    path('course/<str:pk>/', views.course, name="course"),

    path('add-course/', views.addCourse, name="add-course"),
    path('edit-course/<str:pk>/', views.editCourse, name="edit-course"),
    path('delete-course/<str:pk>/', views.deleteCourse, name="delete-course"),

    path('timetable/', views.timetable, name="timetable"),
    #path('generate_timetable', views.generate, name='generate'),

    #path('timetable_generation/', views.timetable, name='timetable'),
    #path('timetable_generation/render/pdf', views.Pdf, name='pdf'),


    #path('ajax/get_lecturerooms/', views.get_lecturerooms, name='get_lecturerooms'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 