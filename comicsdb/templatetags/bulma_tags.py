from django import forms, template

register = template.Library()


@register.filter
def add_field_class(field, css_class):
    """adds css class to a field"""
    if len(field.errors) > 0 and 'is-danger' not in css_class:
        # automatically add .is-danger to fields with invalid values
        css_class += ' is-danger'

    if isinstance(field.field.widget, forms.SplitDateTimeWidget):
        # I personally prefer using SplitDateTimeWidget for datetime
        for subfield in field.field.widget.widgets:
            if subfield.attrs.get('class'):
                subfield.attrs['class'] += f' {css_class}'
            else:
                subfield.attrs['class'] = css_class
        return field

    if field.field.widget.attrs.get('class'):
        field.field.widget.attrs['class'] += f' {css_class}'
    else:
        field.field.widget.attrs['class'] = css_class

    return field


@register.filter
def is_field_type(field, field_type):
    """checks field type"""
    match field_type:
        case 'file':
            return isinstance(field.field.widget, forms.FileInput)
        case 'radio':
            return isinstance(field.field.widget, forms.RadioSelect)
        case 'checkbox':
            return isinstance(field.field.widget, forms.CheckboxInput)
        case 'split_dt':
            return isinstance(field.field.widget, forms.SplitDateTimeWidget)
        case 'input':
            return isinstance(field.field.widget, (
                forms.TextInput,
                forms.NumberInput,
                forms.EmailInput,
                forms.PasswordInput,
                forms.URLInput,
                forms.SplitDateTimeWidget,
            ))
        case 'textarea':
            return isinstance(field.field.widget, forms.Textarea)
        case 'select':
            return isinstance(field.field.widget, forms.Select)
        case 'any_datetime':
            return isinstance(field.field.widget, (
                forms.DateInput,
                forms.TimeInput,
                forms.DateTimeInput,
                forms.SplitDateTimeWidget
            ))  # there is also forms.SplitHiddenDateTimeWidget, but we don't need to check that one imo
        case _:
            raise ValueError(f"Unsupported field_type on |is_field_type:'{field_type}'")


@register.filter
def is_multiple(field):
    """checks multiple field"""
    return (
            isinstance(field.field.widget, forms.CheckboxSelectMultiple) or
            isinstance(field.field.widget, forms.SelectMultiple)
    )


@register.filter
def bulma_message_tag(tag):
    """
    messages use type "error", while bulma use class "danger"
    """
    return {
        'error': 'danger'
    }.get(tag, tag)
