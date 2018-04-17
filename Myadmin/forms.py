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
            # if field_name in obj_all_model_and_display.readonly_fields:
            #     field_obj.widget.attrs['disabled'] = 'disabled'
                # if
            print hasattr(obj_all_model_and_display, "is_add_form")
            if not hasattr(obj_all_model_and_display, "is_add_form"):  # 代表这是添加form,不需要disabled
                if field_name in obj_all_model_and_display.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

            if hasattr(obj_all_model_and_display, "clean_%s" % field_name):
                field_clean_func = getattr(obj_all_model_and_display, "clean_%s" % field_name)
                setattr(cls, "clean_%s" % field_name, field_clean_func)

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
        if self.instance.id:
            for filed in obj_all_model_and_display.readonly_fields:
                filed_val = getattr(self.instance, filed)  # 这个是数据库的值
                filed_val_from_web = self.cleaned_data.get(filed)  # web页的对象
                if hasattr(filed_val, "select_related"):
                    m2m_objs = getattr(filed_val, "select_related")().select_related()  # 服务端的数据的对象
                    print m2m_objs
                    print filed_val_from_web
                    add = m2m_objs.difference(filed_val_from_web)
                    dela = filed_val_from_web.difference(m2m_objs)
                    if add or dela:
                        self.add_error(filed, "%s属性不能修改" % filed)
                    else:
                        continue
                        # m2m_vals = [i[0] for i in m2m_objs.values_list('id')]
                        # set_m2m_vals = set(m2m_vals)
                        # set_m2m_vals_from_frontend = set([i.id for i in filed_val_from_web]) # web页的数据
                        # set_m2m_vals_from_frontend = set([i.id for i in filed_val_from_web]) #
                        # print("m2m",set_m2m_vals,set_m2m_vals_from_frontend)
                        # if set_m2m_vals != set_m2m_vals_from_frontend:
                        #     # error_list.append(ValidationError(
                        #     #     _('Field %(field)s is readonly'),
                        #     #     code='invalid',
                        #     #     params={'field': field},
                        #     # ))
                        #     self.add_error(filed,"readonly field")
                        # continue #m2m
                # print filed_val ,"1"
                # print filed_val_from_web,"2"
                # print filed, filed_val, filed_val_from_web
                if filed_val != filed_val_from_web:
                    error_list.append(ValidationError(_('Filed  %(value)s is Readonly,data should be %(val)s'),
                                                      code='invalid',
                                                      params={'value': filed, 'val': filed_val}))
                    # print self.instance.qq,type(self.instance)
                    # 用户自己的验证
            response = obj_all_model_and_display().default_form_validation(
                self)  # 把self当做参数传递进行 another_self default_form_validation(self,another_self):
            if response:
                error_list.append(response)
            # print response
            if error_list:
                raise ValidationError(error_list)

    class Meta:
        model = obj_all_model_and_display.model
        fields = "__all__"

    # attr = {'Meta': Meta, 'clean':default_clean}
    attr = {'Meta': Meta, '__new__': __new__, 'clean': default_clean}
    # attr = {'Meta': Meta,}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attr)
    # setattr(_model_form_class, '__new__', __new__())
    return _model_form_class
