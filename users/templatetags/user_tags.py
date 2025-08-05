import hashlib

from django import template

register = template.Library()


@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def md5(value):
    if not value:
        return ""
    return hashlib.md5(value.encode("utf-8")).hexdigest()
