# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models


class MyCustomer(admin.ModelAdmin):
    list_display = ('id', 'qq', 'name', 'source', 'consultant', 'content', 'status', 'date')
    list_filter = ('source', 'consultant', 'date')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)
    list_per_page = 5
    readonly_fields = ('qq','content')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


# Register your models here.
admin.site.register(models.Customer, MyCustomer)
admin.site.register(models.Tag)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Course)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.Payment)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Role)
admin.site.register(models.Menu)
