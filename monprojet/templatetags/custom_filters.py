from django import template

register = template.Library()

@register.filter
def filter_quantite(predictions, condition):
    try:
        if condition.startswith('<'):
            value = int(condition[1:])
            return [p for p in predictions if p.quantite_predite < value]
        elif condition.startswith('>='):
            value = int(condition[2:])
            return [p for p in predictions if p.quantite_predite >= value]
    except (ValueError, AttributeError):
        return []
    return []

from django import template

register = template.Library()

@register.filter
def filter_quantite_lt(predictions, value):
    return [p for p in predictions if p.quantite_predite < int(value)]