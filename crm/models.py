# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '市场推广')
                      )
    # SmallIntegerField 小整数
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(verbose_name="转介绍人qq", max_length=64, blank=True, null=True)
    content = models.TextField(verbose_name="咨询详情")
    status_choices = ((0, '已报名'),
                      (1, '未报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=1)
    memo = models.TextField(blank=True, null=True, verbose_name="备注")
    date = models.DateTimeField(auto_now_add=True)
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程")
    consultant = models.ForeignKey("UserProfile", verbose_name="客户经理")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="标签")

    def __unicode__(self):
        return self.qq

    class Meta:
        verbose_name = "客户表(学生)"
        verbose_name_plural = "客户表(学生)"


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32, verbose_name="标签名")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    content = models.TextField(verbose_name="跟进内容")
    intention_choices = ((0, '2周内报名'),
                         (1, '1个月内报名'),
                         (2, '近期无报名计划'),
                         (3, '已在其它机构报名'),
                         (4, '已报名'),
                         (5, '已拉黑'),
                         )
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)
    consultant = models.ForeignKey("UserProfile", verbose_name="账号")
    customer = models.ForeignKey("Customer", verbose_name="客户")

    def __unicode__(self):
        return "<%s : %s>" % (self.customer.qq, self.intention)

    class Meta:
        verbose_name = "客户跟进记录"
        verbose_name_plural = "客户跟进记录"


class Course(models.Model):
    """ 课程表 """
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField(verbose_name="课程")
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField(verbose_name="大纲")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = "课程表"


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=128, unique=True, verbose_name="校区名称")
    addr = models.CharField(max_length=128, verbose_name="校区地址")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"


class ClassList(models.Model):
    """班级表"""
    class_type_choices = ((0, '面授(脱产)'),
                          (1, '面授(周末)'),
                          (2, '网络班')
                          )
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期", blank=True, null=True)
    branch = models.ForeignKey("Branch", verbose_name="校区")
    course = models.ForeignKey("Course")
    teachers = models.ManyToManyField("UserProfile")

    def __unicode__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)
        # return "zhang"

    class Meta:
        # 联合唯一
        unique_together = ('branch', 'course', 'semester')
        verbose_name_plural = "班级"
        verbose_name = "班级"


class CourseRecord(models.Model):
    """上课记录"""
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey("UserProfile", verbose_name="上课老师")
    from_class = models.ForeignKey("ClassList", verbose_name="班级")

    def __unicode__(self):
        return "%s %s" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name_plural = "上课记录"


class StudyRecord(models.Model):
    """学习记录"""
    attendance_choices = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '早退'),
                          )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0, verbose_name="出勤状态")
    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (-100, "COPY"),
                     (0, "N/A"),
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0, verbose_name="分数")
    memo = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    course_record = models.ForeignKey("CourseRecord", verbose_name="上课记录")
    student = models.ForeignKey("Enrollment")

    def __unicode__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)

    class Meta:
        unique_together = ('student', 'course_record')
        verbose_name_plural = "学习记录"


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name_plural = "报名表"


class Payment(models.Model):
    """缴费记录"""
    customer = models.ForeignKey("Customer")
    course = models.ForeignKey("Course", verbose_name="所报课程")
    amount = models.PositiveIntegerField(verbose_name="数额", default=500)
    consultant = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = "缴费记录"


class UserProfile(models.Model):
    """账号表"""
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "系统用户"


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色"


class Menu(models.Model):
    """菜单"""
    name = models.CharField(max_length=32)
    url_type_choices = ((0,'alias'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "菜单"
        verbose_name = "菜单"
