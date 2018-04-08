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
def build_table_row(request,one_obj_django, obj_all_model_and_display):
    row_ele = ""
    for index,filed in enumerate(obj_all_model_and_display.list_display):
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
        if index==0: #add <a></a> tag
            column_data= "<a href='{request_path}/{obj_id}/change' target='_self'>{date}</a>".format(
                request_path=request.path,
                obj_id=one_obj_django.id,
                date=column_data,
            )
        row_ele += "<td>%s</td>" % column_data
    # print row_ele
    return mark_safe(row_ele)


@register.simple_tag
def render_page_ele(loop_counter, query_sets, filter_condtions,order,search):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k, v)
    if not order:
        order=''
    if not search:
        search=''
    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages - 2:  # 显示前2页,或者最后2页
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s&o=%s&q=%s">%s</a></li>''' % (ele_class, loop_counter, filters,order ,search,loop_counter)
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