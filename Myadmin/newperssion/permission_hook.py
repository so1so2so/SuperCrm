#!/usr/bin/env python
# _*_ coding:utf-8 _*_


def view_my_own_customers(request):
    print("running permisionn hook check.....")
    # if str(request.user.id) == request.GET.get('consultant'):
    if request.user.id  >=1:
        print("访问自己创建的用户,允许")
        return True
    else:
        return False
