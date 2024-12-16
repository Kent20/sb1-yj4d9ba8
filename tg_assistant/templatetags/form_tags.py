from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_classes):
    """Add CSS classes to form field"""
    return field.as_widget(attrs={'class': css_classes})