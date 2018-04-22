# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def index(request):
    # print models.Customer._meta.verbose_name
    return render(request, "index.html")

@login_required
def crm(request):
    return HttpResponse("crm")

@login_required
def customer(request):
    # print models.Customer._meta.verbose_name
    return render(request, "customers/customer.html")

def teacher(request):
    return render(request, "teacher/teachers.html")


def sale(request):
    return render(request, "sales/sales.html")
