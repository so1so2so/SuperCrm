# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.decorators import login_required
import forms
import models

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


def payment(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    errors = []
    if request.method == "POST":
        payment_amount = request.POST.get("amount")
        if payment_amount:
            payment_amount = int(payment_amount)

            if payment_amount < 500:
                errors.append("缴费金额不得低于500元")
            else:
                payment_obj = models.Payment.objects.create(
                    customer= enroll_obj.customer,
                    course = enroll_obj.enrolled_class.course,
                    amount = payment_amount,
                    consultant = enroll_obj.consultant
                )
                enroll_obj.contract_approved = True
                enroll_obj.save()


                enroll_obj.customer.status = 0
                enroll_obj.customer.save()
                return redirect("/Myadmin/")
        else:
            errors.append("缴费金额不得低于500元")
    print("errors",errors)
    return render(request,"customers/payment.html",{'enroll_obj':enroll_obj,
                                                'errors':errors})
