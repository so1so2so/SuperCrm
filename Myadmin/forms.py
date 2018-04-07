#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from crm import models
from django.forms import forms, ModelForm
from crm import models


class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


d = type("Foo", (object,), {'name': 123})


# print d


def create_model_form(request, obj_all_model_and_display):
    """动态生成modelform"""

    def __new__(cls, *args, **kwargs):
        # print("base fields", cls.base_fields)
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            if hasattr(field_obj,'max_length') :
                field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length')
            # if
        return ModelForm.__new__(cls)

    class Meta:
        model = obj_all_model_and_display.model
        fields = "__all__"

    attr = {'Meta': Meta, '__new__': __new__}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attr)
    # setattr(_model_form_class, '__new__', __new__)
    return _model_form_class
