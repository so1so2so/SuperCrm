#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# import MySQLdb
# # 打开数据库
# conn = MySQLdb.connect(host='127.0.0.1', user='root',passwd='123456', db='crm')
# # 操作数据库
# do = conn.cursor()
# # 影响了多少行
# ssql = 'select * from test1  where a="bgs"'
# recoun = do.execute(ssql)
#  # 查询的结果
# date = do.fetchall()
# dic={}
# v=[]
# for i in date:
#     # print i[0],i[1]
#     v.append(i[1])
# dic[i[0]]=v
# print dic
# # 关闭数据库
# do.close()
# conn.close()
#
import requests
