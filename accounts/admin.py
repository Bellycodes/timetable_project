from django.contrib import admin
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from allauth.account.models import EmailAddress
from django.contrib.sites.models import Site

from django.contrib.auth.models import User, Group

admin.site.site_header = "TIMETABLE GENERATION"

admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)

# Register your models here
admin.site.unregister(Group)
admin.site.unregister(User)
@admin.register(User)
class Userdmin(admin.ModelAdmin):
    list_display = ['email',]
    ordering = ['email',]
