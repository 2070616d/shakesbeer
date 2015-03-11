from django import template

register = template.Library()

# mostly for the stars
@register.filter(name='times')
def times(number):
    return range(int(number))

@register.filter(name='remainingtimes')
def remainingtimes(number):
    return range(5-int(number))