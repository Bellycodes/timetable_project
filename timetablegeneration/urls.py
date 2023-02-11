from django.contrib import admin
from django.urls import path, include
admin.site.site_header ="TIMETABLE GENERATION SYSTEM"
admin.site.site_title ="TIMETABLE ADMINISTRATION"
admin.site.index_title ="Welcome to the Timetable Administrator site"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]
