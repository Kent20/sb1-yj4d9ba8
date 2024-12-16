"""
Custom template filters for form rendering
"""
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_classes):
    """Add CSS classes to form field"""
    return field.as_widget(attrs={'class': css_classes})

@register.filter(name='with_attrs')
def with_attrs(field, attrs):
    """Add multiple attributes to form field"""
    attrs_dict = {}
    for attr in attrs.split(','):
        if ':' in attr:
            key, value = attr.split(':')
            attrs_dict[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs_dict)