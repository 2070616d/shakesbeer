from django import template

register = template.Library()

# mostly for the stars
@register.filter(name='times')
def times(number):
    return range(int(number+0.5))

@register.filter(name='remainingtimes')
def remainingtimes(number):
    return range(5-int(number+0.5))

@register.inclusion_tag('searchbar.html')
def searchbar(cat=None):
    return {}