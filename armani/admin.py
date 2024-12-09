from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import MentorAdminForm


@admin.register(Mentor)
class MentorsAdmin(admin.ModelAdmin):
    form = MentorAdminForm

    class Media:
        css = {
            'all': ('custom_admin.css',)
        }

    list_display = ['id', 'user']
    filter_vertical = ['services']


# @admin.register(Mentor)
# class MentorsAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'is_mentor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'is_mentor')}),
    )


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', ]
# Register your models here.
