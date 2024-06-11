from django import template
from django.forms import BoundField

register = template.Library()


@register.filter
def add_class(value, arg):
    if isinstance(value, BoundField):
        css_classes = value.field.widget.attrs.get('class', '')
        css_classes = f"{css_classes} {arg}".strip()
        return value.as_widget(attrs={"class": css_classes})
    return value
