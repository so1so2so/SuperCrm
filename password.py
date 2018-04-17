#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
number=48,57
str=65-90,97-122
33-46 58-64  94-96  123-126
"""
daxie = range(65, 90)
daxie += range(97, 123)
import sys
# for i in daxie:
#     print chr(i)


class abc():
    def lsit(self,d):
        return d

g=getattr(abc,'lsit')
s= setattr(abc,'a',g)
# print g
# print abc.a
try:
    d= sys.argv[1]
    print d
except:
    print "请输入命令行参数"
