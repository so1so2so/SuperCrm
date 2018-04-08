#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from crm import models

enable_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filters = []
    list_per_page = 10
    search_fields = []
    ordering = None


class UserProfileAdmin(BaseAdmin):
    list_display = ["id", "name", "roles"]


class BaseisAdmin(BaseAdmin):
    list_display = ["id"]



class CusterAdmin(BaseAdmin):
    # list_display = ["qq", "name"]
    list_display = ['id', 'qq', 'name', 'source', 'content', 'status', 'date', 'tags']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'tags']
    list_per_page = 10
    search_fields = ['qq', 'consultant__name']
    filter_horizontal = ('tags',)
    # ordering = 'qq'
    # model= models.Customer


class ClassListAdmin(BaseAdmin):
    list_display = ["id", "semester", "class_type", "start_date"]
    list_filters = ['class_type']


# admin.site.register(models.Customer, CustomerAdmin)


# 最后形成的数据格式应该是(d)这样 先是app名称,然后里面是一个小字典
# 小字典里面是表名(model的class名称,但是都应该是小写的)和生成注册的时候自定义指定的admin_class对象,这个对象里面配置了可以显示的字段
# 通过表对象拿到app名称 封装在model_obj里面的models.Customer._meta.app_label  crm
# 同样可以拿到表名 models.Customer._meta.model_name  customer

d = {"crm": {"userprofile": "admin_class"}}


def register(model_obj, admin_class=BaseisAdmin):
    app_name = model_obj._meta.app_label
    table_name = model_obj._meta.model_name
    if app_name not in enable_admins:
        enable_admins[app_name] = {}
        # if not admin_class:
        # 数据类型如下
        # d = {"crm": {}}
    # 给admin_class这个类绑定一个属性,当前有list_display属性类似 只不过这个属性是一个model对象 model= models.Customer
    # 就可以用admin_class.model.object.all 拿到这model的值了
    # admin_obj = admin_class()
    # admin_obj.model = model_obj

    admin_class.model = model_obj
    enable_admins[app_name][table_name] = admin_class



register(models.Customer, CusterAdmin)
register(models.UserProfile, UserProfileAdmin)
register(models.ClassList, ClassListAdmin)
register(models.StudyRecord)
# register(models.Course)
# register(models.Branch)
# register(models.CourseRecord)
# register(models.Enrollment)
# register(models.Payment)
# register(models.Role)
# register(models.Menu)
# register(models.CustomerFollowUp)
