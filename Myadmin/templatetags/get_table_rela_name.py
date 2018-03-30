#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#!/usr/bin/env python
# _*_ coding:utf-8 _*_



from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_rela_name(table_obj):
    # print table_obj.model._meta.verbose_name_plural
    return table_obj.model._meta.verbose_name_plural