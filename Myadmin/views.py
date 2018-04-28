#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Myadmin import myadmin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
d_2 = {"crm": {"userprofile": "admin_class"}}
from crm import models, forms
from django.utils.timezone import datetime, timedelta
from forms import create_model_form
from crm.forms import EnrollForm,PaymentForm
import os
from SuperCrm import settings


# Create your views here.
@login_required
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
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    obj_all_model_and_display.is_add_form = True
    new_model_form = create_model_form(request, obj_all_model_and_display)
    if request.method == "GET":
        form_obj = new_model_form()
        return render(request, "Myadmin/table_add.html", locals())
    elif request.method == "POST":
        form_obj = new_model_form(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            # print request.path
            return redirect(request.path.replace("/add/", ''))
        else:
            return render(request, "Myadmin/table_add.html", locals())


def table_edit(request, app_name, table_name, table_id):
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    new_model_form = create_model_form(request, obj_all_model_and_display)
    table_obj = obj_all_model_and_display.model.objects.get(id=table_id)
    if request.method == "GET":
        form_obj = new_model_form(instance=table_obj)
        return render(request, "Myadmin/edit_table.html", locals())
    elif request.method == "POST":
        # print request.POST
        """
        这种方法不好, 外键之类的会拿到对象 用js获取值 直接提交最好
        """
        # post_date=request.POST.copy()
        # for filed in obj_all_model_and_display.readonly_fields:
        #     if hasattr(table_obj, filed):
        #         filed_val = getattr(table_obj, filed)
        #         post_date[filed] = filed_val
        #     else:
        #         raise KeyError("the filed is not rigth")
        # print post_date
        # form_obj = new_model_form(post_date, instance=table_obj)
        #
        form_obj = new_model_form(request.POST, instance=table_obj)
        print form_obj.errors
        if form_obj.is_valid():
            form_obj.save()
            # print request.path
            return redirect(request.path.replace('/' + table_id + '/change/', ''))
        else:
            return render(request, "Myadmin/edit_table.html", locals())


def table_delete(request, app_name, table_name, table_id):
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    # models.Customer.objects.filter(id=1)
    table_obj = obj_all_model_and_display.model.objects.filter(id=table_id)
    print table_obj
    error = '不能删除只读的表'
    if request.method == "POST":
        if not obj_all_model_and_display.readonly_tabs:
            table_obj.delete()
            return redirect(request.path.replace('/' + table_id + '/delete/', ''))
        else:
            return render(request, "Myadmin/table_delete.html", locals())
    else:
        return render(request, "Myadmin/table_delete.html", locals())


def table_filter(request, admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    # print request.GET.items()
    # [(u'status', u''), (u'source', u'1'), (u'id', u''), (u'consult_course', u''), (u'consultant', u'2')] 是列表中的元祖，构造成字典
    for k, v in request.GET.items():
        if k == "page":  # 保留的分页关键字
            continue
        if k == "o":  # 保留的排序关键字
            continue
        if k == "q":  # 保留的搜索的关键字
            continue
        if v:
            filter_conditions[k] = v
    # print filter_conditions
    # print admin_class.model.objects.filter(**filter_conditions),filter_conditions
    # print filter_conditions
    # {u'source': u'1', u'consultant': u'2'} 有值的才加到字典中。
    return admin_class.model.objects.filter(**filter_conditions).order_by(
        admin_class.ordering or '-id'), filter_conditions


def show_table(request, app_name, table_name):
    # 拿到admin_class对象
    print request.user.name
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    # 拿到model对象
    all_obj_django = obj_all_model_and_display.model.objects.all()

    if request.method == "POST":
        # print request.POST
        action = request.POST.get('action')
        selected_ids = request.POST.get('selected_ids')
        print selected_ids.split(',')
        if selected_ids:
            selected_objs = obj_all_model_and_display.model.objects.filter(id__in=selected_ids.split(','))
        else:
            raise KeyError("No object selected")
        if hasattr(obj_all_model_and_display, action):
            action_func = getattr(obj_all_model_and_display, action)
            # print obj_all_model_and_display
            request._admin_action = action
            return action_func(obj_all_model_and_display(), request, selected_objs)
    object_list, filter_condtions = table_filter(request, obj_all_model_and_display)
    order = request.GET.get("o", None)
    if order:
        if order.startswith("-"):
            orders = True
        else:
            orders = False
        # flage = True
        object_list = object_list.order_by(order)
    search = request.GET.get("q", '')
    search_fileds = obj_all_model_and_display.search_fields
    my_search = Q()
    my_search.connector = 'OR'
    if search:
        for search_file in search_fileds:
            my_search.children.append((search_file + '__icontains', search))
        # print my_search
        object_list = object_list.filter(my_search)
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


def password_reset(request, app_name, table_name, table_id):
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    new_model_form = create_model_form(request, obj_all_model_and_display)
    table_obj = obj_all_model_and_display.model.objects.get(id=table_id)
    error = {}
    if request.method == "POST":
        _passwd1 = request.POST.get("passwd1")
        _passwd2 = request.POST.get("passwd2")
        if _passwd1 == _passwd2:
            if len(_passwd1) > 6:
                table_obj.set_password(_passwd1)
                table_obj.save()
                return redirect(request.path.rstrip("passwortd/"))
            else:
                error["password_too_short"] = "密码长度太短"
        else:
            error["invalid"] = "两次输入的密码必须一致"
    return render(request, "Myadmin/password_reset.html", locals())


def enrollment(request, app_name, table_name, table_id):
    obj_all_model_and_display = myadmin.enable_admins[app_name][table_name]
    new_model_form = create_model_form(request, obj_all_model_and_display)
    table_obj = obj_all_model_and_display.model.objects.get(id=table_id)
    next_links = {}
    enroll_obj_id=table_obj.enrollment_set.all()[0].id
    if request.method == "POST":
        emMd = EnrollForm(request.POST)
        if emMd.is_valid():
            # print emMd.cleaned_data
            next_link = 'http://localhost:8000/Myadmin/crm/customer/registration/{enroll_obj_id}'
            try:
                # print table_name
                emMd.cleaned_data[table_name] = table_obj
                # print emMd.cleaned_data
                eroll_obj = models.Enrollment.objects.create(**emMd.cleaned_data)
                next_links["msg"] = next_link.format(enroll_obj_id=eroll_obj.id)
                # next_link = 'http://localhost:8000/crm/customer/registration/{enroll_obj_id}/'
            except IntegrityError as e:
                emMd.add_error("__all__", "该用户已报名")
                enroll_obj_id=table_obj.enrollment_set.all()[0].id
                next_links["msg"] = next_link.format(enroll_obj_id=enroll_obj_id)
                # print eroll_obj
    else:
        emMd = EnrollForm()
    return render(request, 'Myadmin/enrollment.html', locals())


def stu_registration(request, app_name, table_name, table_id):
    enroll_obj = models.Enrollment.objects.get(id=table_id)
    status=0
    if request.method == "POST":
        if request.is_ajax():
            # (u'ajax post, ', <MultiValueDict: {u'file': [<InMemoryUploadedFile: BigShare_18038_19689_1075688650.jpg (image/jpeg)>]}>)
            print("ajax post, ", request.FILES)
            enroll_data_dir = "%s/%s" % (settings.ENROLLED_DATA, table_id)
            # J:\Djangostyle\SuperCrm/enrolled_data//10
            print enroll_data_dir
            if not os.path.exists(enroll_data_dir):
                os.makedirs(enroll_data_dir)

            for k, file_obj in request.FILES.items():
                with open("%s/%s" % (enroll_data_dir, file_obj.name), "wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
            return HttpResponse("success")
        customer_form = forms.CustomerForm(request.POST, instance=enroll_obj.customer)
        if customer_form.is_valid():
            customer_form.save()
            enroll_obj.contract_agreed = True
            enroll_obj.save()
            return render(request, "Myadmin/stu_registration.html", {"status": 1})
    else:
        # 用户已同意
        if enroll_obj.contract_agreed == True:
            status = 1
        else:
            status = 0
        customer_form = forms.CustomerForm(instance=enroll_obj.customer)
    return render(request, "Myadmin/stu_registration.html",
                  {"customer_form": customer_form,
                   "enroll_obj": enroll_obj,
                   "status": status})


