# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
import models


# Create your views here.
def sale_index(request):
    return render(request, "sales/sales.html")


def customer(request):
    # print models.Customer._meta.verbose_name
    return render(request, "customers/customer.html")


