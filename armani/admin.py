from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

@admin.register(Mentor)
class MentorsAdmin(admin.ModelAdmin):
    list_display = ['id','user']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'is_mentor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ( 'phone', 'is_mentor')}),
    )
# Register your models here.
