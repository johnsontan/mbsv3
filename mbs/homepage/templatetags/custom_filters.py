from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    if hasattr(field, 'field'):  # Check if it's a bound field
        existing_classes = field.field.widget.attrs.get('class', '')
        field.field.widget.attrs['class'] = f"{existing_classes} {css}".strip()
        return field
    return field
