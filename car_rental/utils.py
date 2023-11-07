def set_form_styles(form_fields):
    field_types = {
        'CharField': {
            'field': 'form-control',
        },
        'PasswordField': {
            'field': 'form-control',
        },
        'BooleanField': {
            'field': 'form-check-input',
        },
        'EmailField': {
            'field': 'form-control',
        },
        'SetPasswordField': {
            'field': 'form-control',
        },
    }
    for _, field in form_fields.items():
        if field.__class__.__name__ in field_types.keys():
            field.widget.attrs.update(
                {
                    'class': field_types[field.__class__.__name__]['field'],
                },
            )
