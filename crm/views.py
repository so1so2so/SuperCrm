# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
import models


# Create your views here.
def index(request):
    # print models.Customer._meta.verbose_name
    return render(request, "index.html")


def customer(request):
    # print models.Customer._meta.verbose_name
    return render(request, "customers/customer.html")


def students(request):
    return render(request, "students/students.html")


def teacher(request):
   return render(request, "teacher/teachers.html")


def sale(request):
    return render(request, "sales/sales.html")