def check_forms(line, filename, options):
    info = []
    if filename == 'forms.py':
        if 'PasswordInput' in line and 'render_value=False' in line:
            info.append("PasswordInput no long requires explicit render_value=False.")
        if 'FileInput' in line:
            info.append('Consider using ClearableFileInput instead of FileInput.')
    return [], [], info


def check_models(line, filename, options):
    warnings = []
    if filename == 'models.py':
        if 'XMLField' in line:
            warnings.append('XMLField is deprecated in Django 1.3. Use TextField instead.')
        if 'verify_exists' in line:
            warnings.append('verify_exists is deprecated in Django 1.3.')
    return warnings, [], []


def check_generic_views(line, filename, options):
    warnings = []
    if 'django.views.generic' in line and \
       ('create_update' in line or \
       'date_based' in line or \
       'list_detail' in line or \
       'simple' in line):
        warnings.append('Function-based generic views are deprecated in Django 1.3.')
    return warnings, [], []


def check_localflavor(line, filename, options):
    warnings = []
    if filename == 'forms.py':
        if 'USStateField' in line and 'choices' not in line:
            warnings.append('USStateField default choices have changed. Consider setting explicit choices.')
    return warnings, [], []


def check_profanities_list(line, filename, options):
    warnings = []
    if 'PROFANITIES_LIST' in line:
        warnings.append('Use of PROFANITIES_LIST is discouraged; the default is now an empty value.')
    return warnings, [], []


def check_response_template(line, filename, options):
    warnings = []
    if 'test' in filename:
        if 'resp' in line and '.template' in line:
            warnings.append('TestClient.response.template is deprecated in Django 1.3. Use TestClient.response.templates instead.')
    return warnings, [], []


def check_compatcookie(line, filename, options):
    warnings = []
    if 'django.http' in line and 'CompatCookie' in line:
        warnings.appened('django.http.CompatCookie is deprecated in Django 1.3. Use django.http.SimpleCookie instead.')
    return warnings, [], []


def check_django_13(line, filename, options):
    warnings = []
    info = []
    errors = []

    for check in (check_forms, check_models, check_generic_views,
                  check_localflavor, check_profanities_list,
                  check_response_template, check_compatcookie):
        warn, err, inf = check(line, filename, options)
        warnings += warn
        info += inf
        errors += err

    return warnings, errors, info


rules = [
    {'long_option': '--django-13',
     'action': 'store_true',
     'dest': 'django_13',
     'help': 'Check for changes and deprecations in Django 1.3.',
     'callback': check_django_13,
     'enabled': lambda options: options.django_13,}
]
