# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from crm import models

from Myadmin import myadmin

d_2 = {"crm": {"userprofile": "admin_class"}}


# Create your views here.
def index(request):
    # print models.Customer._meta.verbose_name
    # d = models.Customer.objects.all()
    obj_all = myadmin.enable_admins
    return render(request, "Myadmin/table_index.html", {"obj_all": obj_all})


def show_app(request, app_name):
    return HttpResponse("show_app")


def table_add(request, app_name, table_name):
    return HttpResponse("table_add")


def table_edit(request, app_name, table_name):
    return HttpResponse("edit")


def show_table(request, app_name, table_name):
    obj_all = myadmin.enable_admins

    for i in myadmin.enable_admins.itervalues():
        for obj_model in i.itervalues():
            allmodel=obj_model.model.objects.all()
            print "---------------"
            all_key =obj_model.__dict__
            if dict(all_key).has_key("list_display"):
                print all_key["list_display"]
    return render(request,"Myadmin/show_table.html",{"obj_all": obj_all})
