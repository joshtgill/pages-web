from django import template


register = template.Library()


@register.filter(name='formatPrice')
def formatPrice(price):
    if int(price) == price:
        return int(price)

    return format(price, '.2f')


@register.filter(name='formatDays')
def formatDays(repeatingOccurence):
    repeatingDays = []
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        if repeatingOccurence.get(day):
            repeatingDays.append(day.capitalize())

    return ', '.join(repeatingDays)
