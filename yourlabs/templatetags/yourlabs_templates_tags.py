import re

from django import template

register = template.Library()


@register.filter
def cbv_to_urlname_suffix(name):
    if name[-4:] == 'View':
        name = name[:-4]
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
