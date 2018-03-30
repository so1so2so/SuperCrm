#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from crm import models

enable_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filter = []


class UserProfileAdmin(BaseAdmin):
    list_display = ["name"]


class CusterAdmin(BaseAdmin):
    list_display = ["qq", "name"]

    # model= models.Customer


# admin.site.register(models.Customer, CustomerAdmin)



# 最后形成的数据格式应该是(d)这样 先是app名称,然后里面是一个小字典
# 小字典里面是表名(model的class名称,但是都应该是小写的)和生成注册的时候自定义指定的admin_class对象,这个对象里面配置了可以显示的字段
# 通过表对象拿到app名称 封装在model_obj里面的models.Customer._meta.app_label  crm
# 同样可以拿到表名 models.Customer._meta.model_name  customer

d = {"crm": {"userprofile": "admin_class"}}


def register(model_obj, admin_class=None):
    app_name = model_obj._meta.app_label
    table_name = model_obj._meta.model_name
    if app_name not in enable_admins:
        enable_admins[app_name] = {}
        # 数据类型如下
        # d = {"crm": {}}
    # 给admin_class这个类绑定一个属性,当前有list_display属性类似 只不过这个属性是一个model对象 model= models.Customer
    # 就可以用admin_class.model.object.all 拿到这model的值了
    # admin_obj = admin_class()
    # admin_obj.model = model_obj
    admin_class.model=model_obj
    enable_admins[app_name][table_name] = admin_class


register(model_obj=models.Customer, admin_class=CusterAdmin)
register(model_obj=models.UserProfile, admin_class=UserProfileAdmin)
# register(model_obj=models.ClassList, admin_class=UserProfileAdmin)
# register(model_obj=models.Course, admin_class=UserProfileAdmin)
# register(model_obj=models.CourseRecord, admin_class=UserProfileAdmin)
# register(model_obj=models.Branch, admin_class=UserProfileAdmin)