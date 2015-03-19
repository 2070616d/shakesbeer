from django import template

register = template.Library()

# mostly for the stars
@register.filter(name='times')
def times(number):
    return range(1, int(number+0.5)+1)

@register.filter(name='remainingtimes')
def remainingtimes(number):
    return range(int(number+1.5), 6)

@register.inclusion_tag('searchbar.html')
def searchbar(cat=None):
    return {}
