# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from crm import models

from Myadmin import myadmin

d_2 = {"crm": {"userprofile": "admin_class"}}


# Create your views here.
def index(request):
    # print models.Customer._meta.verbose_name
    d= ('id', 'qq', 'name', 'source', 'consultant', 'content', 'status', 'date')
    d = models.Customer.objects.all().values_list(*d)
    print d
    obj_all = myadmin.enable_admins
    return render(request, "Myadmin/table_index.html", {"obj_all": obj_all})


def show_app(request, app_name):
    return HttpResponse("show_app")


def table_add(request, app_name, table_name):
    return HttpResponse("table_add")


def table_edit(request, app_name, table_name,table_id):
    return HttpResponse("edit")


def show_table(request, app_name, table_name):
    obj_all = myadmin.enable_admins[app_name][table_name]
    # print obj_all.list_display
    # print type(obj_all.list_display)
    this_obj=obj_all.model.objects.all()
    if dict(obj_all.__dict__).has_key("list_display"):
        list_filed= obj_all.__dict__["list_display"]
        this_obj=obj_all.model.objects.values_list(*list_filed)

    # print this_obj
    for i in this_obj:
        for j in i:
            print j



    # for i in range(len(obj_all.list_display)):
    #     # print i
    #     shot = obj_all.list_display[i]
    #     # print shot
    #     rela_row_dat=[]
    #     for j in this_obj:
    #         # print j[shot]
    #         pass
    #     rela_row_dat.append(j[shot])
    # rela_row_dat_all.append(rela_row_dat)
    # print rela_row_dat_all
    return render(request,"Myadmin/show_table.html",locals())