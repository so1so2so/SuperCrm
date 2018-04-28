#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django import template

from django.utils.safestring import mark_safe

register = template.Library()
from django.db.models import Sum

@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_records = enroll_obj.studyrecord_set.\
        filter(course_record__from_class_id=enroll_obj.enrolled_class.id)

    # for record in study_records:
    #     print('-->',record)
    return study_records.aggregate(Sum('score'))