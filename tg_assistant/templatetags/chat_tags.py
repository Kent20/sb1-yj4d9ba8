"""
Custom template tags for chat functionality
"""
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def chat_status_badge(chat):
    """Render chat status badge"""
    if chat.is_active:
        return mark_safe('<span class="text-green-500">●</span> Активен')
    return mark_safe('<span class="text-gray-500">○</span> Неактивен')

@register.filter
def unread_badge(count):
    """Render unread messages badge"""
    if count > 0:
        return mark_safe(
            f'<span class="ml-2 px-2 py-1 text-xs font-medium rounded-full '
            f'bg-blue-100 text-blue-800">{count} непрочитано</span>'
        )
    return ''