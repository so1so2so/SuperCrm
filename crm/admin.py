# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import render, HttpResponse, redirect


class MyCustomer(admin.ModelAdmin):
    list_display = ('id', 'qq', 'name', 'source', 'consultant', 'content', 'status', 'date')
    list_filter = ('source', 'consultant', 'date')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)
    list_per_page = 5
    readonly_fields = ('qq', 'content')


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('email',)




class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin', 'is_active',)
    list_filter = ('is_admin',)
    # 页面上分了几块
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('name','stu_account',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', "is_superuser", "groups", "user_permissions", 'roles')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("groups", "user_permissions",)


# Register your models here.
class AdminCourseRecord(admin.ModelAdmin):
    list_display = ('from_class', 'teacher', 'day_num', 'has_homework',)

    def make_published(self, request, queryset):
        print self, request, queryset
        if len(queryset) > 1:
            return HttpResponse("只能选择一个班级")
        new_obj_list=[]
        for i in queryset[0].from_class.enrollment_set.all():
            # 拿到学生ID
            print i
            new_obj_list.append(models.StudyRecord(
                student=i,
                attendance=0,
                score=0,
                course_record=queryset[0]
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)
        except Exception as e:
            return HttpResponse("批量初始化记录失败,请检查改节课是否有对应的学习记录")
        return redirect('/admin/crm/studyrecord/?course_record__id__exact={classes}'.format(classes=queryset[0].id))

    make_published.short_description = "初始化上课记录"
    actions = ['make_published']


# class AdminStudyRecord(admin.ModelAdmin):
#     list_display = ('student','attendance', 'score', 'course_record', )
#     list_filter=('attendance','course_record',)
#     list_editable = ('score','attendance',)
admin.site.register(models.Customer, MyCustomer)
admin.site.register(models.Tag)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Course)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord, AdminCourseRecord)
admin.site.register(models.StudyRecord,)
admin.site.register(models.Enrollment)
admin.site.register(models.Payment)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.ContractTemplate)
