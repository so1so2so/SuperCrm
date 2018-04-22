#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.forms import ModelForm
from crm import models


class EnrollForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model = models.Enrollment
        fields = ['customer', 'enrolled_class', 'consultant']
