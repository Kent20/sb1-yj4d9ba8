"""
Custom template tags for dialogue functionality
"""
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def message_status(dialogue):
    """Render message status indicator"""
    if dialogue.is_outgoing:
        return mark_safe('<span class="text-blue-500">●</span> Отправлено')
    return mark_safe('<span class="text-gray-500">○</span> Получено')

@register.filter
def response_status(response):
    """Render response status"""
    if response.is_used:
        return mark_safe(
            '<span class="inline-flex items-center px-2 py-1 rounded-full '
            'bg-green-100 text-green-800 text-xs font-medium">'
            '<i class="fas fa-check mr-1"></i> Использован</span>'
        )
    return ''