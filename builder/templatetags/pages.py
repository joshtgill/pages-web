from django import template


register = template.Library()


@register.filter(name='pluralize')
def pluralize(value):
    return '{}\''.format(value) if value.endswith('s') else '{}\'s'.format(value)
