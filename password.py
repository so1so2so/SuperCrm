#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
number=48,57
str=65-90,97-122
33-46 58-64  94-96  123-126
"""
daxie = range(65, 90)
daxie += range(97, 123)

# for i in daxie:
#     print chr(i)


def check_str():
    aimput=str(input("请输入密码"))
    for i in aimput:
        num=ord(i)
        print num
check_str()