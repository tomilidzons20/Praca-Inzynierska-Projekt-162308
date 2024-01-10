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
        'IntegerField': {
            'class': 'form-control',
        },
        'FloatField': {
            'class': 'form-control',
        },
        'DateField': {
            'class': 'form-control',
        },
        'DateTimeField': {
            'class': 'form-control',
        },
        'DurationField': {
            'class': 'form-control',
        },
        'MoneyField': {
            'class': 'form-control',
        },
        'TextField': {
            'class': 'form-control',
        },
    }

    for _, field in form_fields.items():
        if field.__class__.__name__ in field_types.keys():
            field_class = field_types[field.__class__.__name__]['class']
            field.widget.attrs.update(
                {
                    'class': field_class,
                },
            )
