from django import template


register = template.Library()


@register.filter(name='formatPrice')
def formatPrice(price):
    if int(price) == price:
        return int(price)

    return format(price, '.2f')
