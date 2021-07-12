from django import template


register = template.Library()


@register.filter(name='buildPageTitle')
def buildPageTitle(pageName):
    if not pageName:
        return 'Pages'

    return 'Pages | {}'.format(pageName)
