from cProfile import label

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# from .forms import MentorAdminForm


@admin.register(Articles)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager']


# @admin.register(Mentor)
# class MentorsAdmin(admin.ModelAdmin):
#     form = MentorAdminForm
#
#     class Media:
#         css = {
#             'all': ('custom_admin.css',)
#         }
#
#     list_display = ['id', 'user']
#     filter_vertical = ['services']


# @admin.register(Mentor)
# class MentorsAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'Photo']  # اضافه کردن Photo به لیست نمایش
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'Photo','job_position','services','city','country')}),  # اضافه کردن Photo به فیلدهای فرم
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'Photo','job_position','services','city','country')}),  # اضافه کردن Photo هنگام ثبت کاربر
    )


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', ]
# Register your models here.
