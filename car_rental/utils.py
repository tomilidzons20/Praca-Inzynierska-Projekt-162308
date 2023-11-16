def set_form_styles(form_fields):
    field_types = {
        'CharField': {
            'class': 'form-control',
        },
        'PasswordField': {
            'class': 'form-control',
        },
        'BooleanField': {
            'class': 'form-check-input',
        },
        'EmailField': {
            'class': 'form-control',
        },
        'SetPasswordField': {
            'class': 'form-control',
        },
        'PhoneNumberField': {
            'class': 'form-control',
        },
        'ImageField': {
            'class': 'form-control',
        },
    }

    for _, field in form_fields.items():
        if field.__class__.__name__ in field_types.keys():
            field.widget.attrs.update(
                {
                    'class': field_types[field.__class__.__name__]['class'],
                },
            )
