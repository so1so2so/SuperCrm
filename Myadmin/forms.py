#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from crm import models
from django.forms import forms, ModelForm
from crm import models
from  django.forms import ValidationError
from django.utils.translation import ugettext as _


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
            if hasattr(field_obj, 'max_length'):
                field_obj.widget.attrs['maxlength'] = getattr(field_obj, 'max_length')
            if field_name in obj_all_model_and_display.readonly_fields:
                field_obj.widget.attrs['disabled'] = 'disabled'
                # if
        return ModelForm.__new__(cls)

    def default_clean(self):
        """
        给所有form加一个clean验证 self 里面就包含的所有提交的html
        :param self:
        :return:
        """
        # print "开始验证" ,obj_all_model_and_display.readonly_fields
        # 提交的数据在self里面 ,在数据库里面进行查询,找出值进行对比
        # print dir(self.instance)
        # print self.instance.qq #提交之前的
        # print self.cleaned_data['qq'] #提交之后的
        error_list = []
        for filed in obj_all_model_and_display.readonly_fields:
            filed_val = getattr(self.instance, filed)  # 这个是数据库的值
            filed_val_from_web = self.cleaned_data.get(filed)
            # print filed_val ,"1"
            # print filed_val_from_web,"2"
            # print filed, filed_val, filed_val_from_web
            if filed_val != filed_val_from_web:
                    error_list.append(ValidationError(('Filed  %(value)s is Readonly,data should be %(val)s'),
                                      code='invalid',
                                      params={'value': filed, 'val': filed_val}))
                # print self.instance.qq,type(self.instance)
        if error_list:
            raise ValidationError(error_list)
    class Meta:
        model = obj_all_model_and_display.model
        fields = "__all__"

    # attr = {'Meta': Meta, 'clean':default_clean}
    attr = {'Meta': Meta, '__new__': __new__, 'clean': default_clean}
    # attr = {'Meta': Meta,}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attr)
    # setattr(_model_form_class, '__new__', __new__(ModelForm))
    return _model_form_class
