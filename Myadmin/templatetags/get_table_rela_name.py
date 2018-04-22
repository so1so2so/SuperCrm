#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django import template

from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_rela_name(table_obj):
    table_name = table_obj.model._meta.verbose_name_plural or table_obj.verbose_name
    if not table_name:
        table_name = table_obj.model._meta.model_mame
    return table_name


@register.simple_tag
def get_chinese_name(table_obj):
    if hasattr(table_obj._meta, 'verbose_name_plural'):
        return table_obj._meta.verbose_name_plural
    elif hasattr(table_obj._meta, 'verbose_name'):
        return table_obj._meta.verbose_name
    else:
        return table_obj._meta.model_mame


@register.simple_tag
def build_table_row(request, one_obj_django, obj_all_model_and_display):
    row_ele = ""
    for index, filed in enumerate(obj_all_model_and_display.list_display):
        field_obj = one_obj_django._meta.get_field(filed)
        if field_obj.choices:  # choices type
            column_data = getattr(one_obj_django, "get_%s_display" % filed)()
        else:
            column_data = getattr(one_obj_django, filed)
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if type(field_obj).__name__ == "ManyToManyField":
            all_date = getattr(field_obj, 'get_choices')()[1:]
            for choice_item in all_date:
                if str(choice_item[0]) == one_obj_django:
                    pass
        if index == 0:  # add <a></a> tag
            column_data = "<a href='{request_path}/{obj_id}/change' target='_self'>{date}</a>".format(
                request_path=request.path,
                obj_id=one_obj_django.id,
                date=column_data,
            )
        row_ele += "<td>%s</td>" % column_data
    # print row_ele
    return mark_safe(row_ele)


@register.simple_tag
def render_page_ele(loop_counter, query_sets, filter_condtions, order, search):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k, v)
    if not order:
        order = ''
    if not search:
        search = ''
    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages - 2:  # 显示前2页,或者最后2页
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s&o=%s&q=%s">%s</a></li>''' % (
            ele_class, loop_counter, filters, order, search, loop_counter)
        return mark_safe(ele)

    if abs(query_sets.number - loop_counter) <= 1:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (ele_class, loop_counter, filters, loop_counter)
        return mark_safe(ele)
    return ''


@register.simple_tag
def render_filter_ele(condtion, obj_all_model_and_display, filter_condtions):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' % condtion
    # 拿到每一个需要filter的值
    field_obj = obj_all_model_and_display.model._meta.get_field(condtion)
    if field_obj.choices:
        selected = ''
        # 这个循环会循环所有的choices ((0, '已报名'), (1, '未报名'), (2, '已退学'), (3, '其他'))
        for choice_item in field_obj.choices:
            # 判断filter_condtions这个字典 {u'source': u'1', u'consultant': u'2'}
            # print("choice", choice_item, filter_condtions.get(condtion), type(filter_condtions.get(condtion)))
            # 如果前端传递来的值的
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ == "ManyToManyField":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            # print filter_condtions.get(condtion)
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def change_order(column):
    if column.startswith("-"):
        column = column.strip("-")
    else:
        column = "-%s" % column
    return column


@register.simple_tag
def get_all_m2m_list(obj_all_model_and_display, field, form_obj):
    """

    :param obj_all_model_and_display:
    :param field:
    :param form_obj:
    :return: 返还m2m所有待选数据
    """
    # models.Customer.tags.rel.to.objects.all()
    # obj_all_model_and_display.model=models.Customer
    # print obj_all_model_and_display.model
    if hasattr(obj_all_model_and_display.model, field.name):
        field_all_obj = getattr(obj_all_model_and_display.model, field.name).rel.to.objects.all()
        # print field_all_obj
        # 相当于field_obj =models.Customer.tags.
        #     类似 getattr(d,'tags').rel.to.objects.all()
        #     print field_all_obj.intersection(field_select_obj)
        #     "返还全部的减去待选的"
    if hasattr(form_obj.instance, field.name):
        field_select_obj = getattr(form_obj.instance, field.name).all()
        return field_all_obj.difference(field_select_obj)
    else:
        return field_all_obj
        # return (field_select_obj|field_all_obj).distinct()


@register.simple_tag
def print_obj_(obj):
    return obj.instance


@register.simple_tag
def get_select_m2m_list(form_obj, field):
    """

    :param form_obj:
    :param field:
    :return: {{ form_obj.instance.tags.all }}
    form_obj= new_model_form(instance=table_obj)
    返还已选择的
    """
    if hasattr(form_obj.instance, field.name):
        field_select_obj = getattr(form_obj.instance, field.name)
        return field_select_obj.all()
    else:
        return ""


def recursive_related_objs_lookup(objs):
    print "objs", objs
    # model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li> %s: %s </li>''' % (obj._meta.verbose_name, obj.__unicode__().strip("<>"))
        ul_ele += li_ele

        # for local many to many
        # print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many:  # 把所有跟这个对象直接关联的m2m字段取出来了
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj, m2m_field.name)  # getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():  # customer.tags.select_related()
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__unicode__().strip("<>"))
                sub_ul_ele += li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  # 最终跟最外层的ul相拼接

        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel", accessor_obj, related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele = "<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__unicode__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                # 上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                    target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    print("one to one i guess:", accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) > 0:
                    # print("\033[31;1mdeeper layer lookup -------\033[0m")
                    # nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele += "</ul>"
    return ul_ele


@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    # objs = [objs]  # fake
    # if objs:
    # model_class = objs[0]._meta.model  # <class 'crm.models.Customer'>
    # mode_name = objs[0]._meta.model_name  # customer
    return mark_safe(recursive_related_objs_lookup(objs))


@register.simple_tag
def display_no_exist(one_obj_django, filed,table_name):
    return mark_safe('''<a href="%s/%s/%s">点击报名</a>''' % (str(table_name),one_obj_django.id, filed))


@register.simple_tag
def get_filed_chinese_name(column, obj_all_model_and_display):
    """
    models.Customer._meta.get_field('tags').verbose_name
    :param column:
    :param obj_all_model_and_display:
    :return:
    """
    # print obj_all_model_and_display.model._meta.get_field('tags').verbose_name

    chinese_chinses_obj = obj_all_model_and_display.model._meta.get_field(column)
    return chinese_chinses_obj.verbose_name
