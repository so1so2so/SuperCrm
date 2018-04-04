# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Myadmin import myadmin

d_2 = {"crm": {"userprofile": "admin_class"}}
from crm import models

# Create your views here.
def index(request):
    # for i in range(20):
    #     models.Customer.objects.create(
    #         qq="103793045" + str(i),
    #         name="张" + str(i) + "帅",
    #         source=5,
    #         content="没戏了",
    #         status=0,
    #         consult_course=models.Course.objects.get(id=1),
    #         consultant=models.UserProfile.objects.get(id=1),
    #         # tags=1,
    #     )
    obj_all = myadmin.enable_admins
    return render(request, "Myadmin/table_index.html", {"obj_all": obj_all})


def show_app(request, app_name):
    return HttpResponse("show_app")


def table_add(request, app_name, table_name):
    return HttpResponse("table_add")


def table_edit(request, app_name, table_name, table_id):
    return HttpResponse("edit")


def table_filter(request, admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    # print request.GET.items()
    # [(u'status', u''), (u'source', u'1'), (u'id', u''), (u'consult_course', u''), (u'consultant', u'2')] 是列表中的元祖，构造成字典
    for k, v in request.GET.items():
        if v:
            filter_conditions[k] = v
    # print admin_class.model.objects.filter(**filter_conditions),filter_conditions
    # print filter_conditions
    # {u'source': u'1', u'consultant': u'2'} 有值的才加到字典中。
    return admin_class.model.objects.filter(**filter_conditions), filter_conditions


def show_table(request, app_name, table_name):
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    all_obj_django = obj_all_model_and_display.model.objects.all()
    # if dict(obj_all.__dict__).has_key("list_display"):
    #     list_filed = obj_all.__dict__["list_display"]
    #     for filed in list_filed:
    #         check_choise = obj_all.model._meta.get_field(filed)
    #         # print check_choise
    #         if check_choise.choices:
    #             print check_choise.choices
    #     this_obj = obj_all.model.objects.values_list(*list_filed)
    object_list, filter_condtions = table_filter(request, obj_all_model_and_display)
    paginator = Paginator(object_list, obj_all_model_and_display.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    return render(request, "Myadmin/show_table.html", locals())
